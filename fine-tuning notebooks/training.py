#NOTE:  This must be the first call in order to work properly!
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)



import os
import fastai
from fastai import *
from fastai.vision import *
from fastai.callbacks.tensorboard import *
from fastai.vision.gan import *
from deoldify.generators import *
from deoldify.critics import *
from deoldify.dataset import *
from deoldify.loss import *
from deoldify.save import *
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFile


path = Path('./data') #-> Sets the base path for data storage.
path_hr = path #->  path for high resolution images
path_lr = path/'bandw' #-> path for low resolution (grayscale) images

proj_id = 'ArtisticModel' #-> Porject id for folder naming

gen_name = proj_id + '_gen' #->['ArtisticModel_gen']  Creates a name for the generator model based on the project ID.
pre_gen_name = gen_name + '_0' #->['ArtisticModel_gen_0']  Creates a name for the initial version of the generator model.
crit_name = proj_id + '_crit' # Creates a name for the critic (or discriminator) model.

name_gen = proj_id + '_image_gen' #-> Creates a folder name for the generated images.
path_gen = path/name_gen #-> Sets the path for the generated images

TENSORBOARD_PATH = Path('data/tensorboard/' + proj_id)

nf_factor = 1.5
pct_start = 1e-8


def get_data(bs:int, sz:int, keep_pct:float): #->This function prepares the data for training the colorization model.
    data = get_colorize_data(sz=sz, bs=bs, crappy_path=path_lr, good_path=path_hr,
                            random_seed=None, keep_pct=keep_pct)
    print(data)
    print(f"Number of items: {len(data.items)}")
    return data

def get_crit_data(classes, bs, sz): #-> function prepares data for training the critic (discriminator) model.
    src = ImageList.from_folder(path, include=classes, recurse=True).split_by_rand_pct(0.1, seed=42)
    ll = src.label_from_folder(classes=classes)
    data = (ll.transform(get_transforms(max_zoom=2.), size=sz)
        .databunch(bs=bs).normalize(imagenet_stats))
    return data

def create_training_images(fn): #-> This function creates grayscale versions of high-resolution images.
    dest = path_lr/fn.relative_to(path_hr)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img = PIL.Image.open(fn).convert('LA').convert('RGB')
    img.save(dest)

def save_preds(dl): #-> This function saves the predictions of the generator model.
    i=0
    names = dl.dataset.items

    for b in dl:
        preds = learn_gen.pred_batch(batch=b, reconstruct=True)
        for o in preds:
            o.save(path_gen/names[i].name)
            i += 1

def save_gen_images(): #-> This function generates and saves images using the generator model.
    if path_gen.exists(): shutil.rmtree(path_gen)
    path_gen.mkdir(exist_ok=True)
    data_gen = get_data(bs=bs, sz=sz, keep_pct=0.085)
    save_preds(data_gen.fix_dl)
    PIL.Image.open(path_gen.ls()[0])
    
    
# function used for creating grayscale image of colorful image
if not path_lr.exists():
    path_lr.mkdir(parents=True)
    il = ImageList.from_folder(path_hr)
    print(il.items)
    for fn in il.items:
        create_training_images(fn)

##############################
# 64
##############################
bs=64 #-> batch size
sz=64 #-> image size
keep_pct=1.0 #-> percentage of images to keep

data_gen = get_data(bs=bs, sz=sz, keep_pct=keep_pct) #-> loads the data using the get_data function with the specified batch size, image size, and data percentage.

learn_gen = gen_learner_deep(data=data_gen, gen_loss=FeatureLoss(), nf_factor=nf_factor) #-> creates the generator learner using the gen_learner_deep function.
learn_gen.callback_fns.append(partial(ImageGenTensorboardWriter, base_dir=TENSORBOARD_PATH, name='GenPre')) #-> callback function to log training progress to TensorBoard.
learn_gen.fit_one_cycle(1, pct_start=0.8, max_lr=slice(1e-3)) #-> trains the generator model for one cycle, learning rate starts at 80% of the maximum learning rate (pct_start=0.8)
learn_gen.save(pre_gen_name) #-> saves the generator model.

learn_gen.unfreeze() #->  unfreezes the model layers, allowing all layers to be fine-tuned.

learn_gen.fit_one_cycle(1, pct_start=pct_start,  max_lr=slice(3e-7, 3e-4)) #-> fine-tunes the generator model for one cycle.
learn_gen.save(pre_gen_name) #-> saves the generator model.


##############################
# 128
##############################
bs=22 #-> batch size
sz=128 #-> image size
keep_pct=1.0 #-> percentage to look after 
learn_gen.data = get_data(sz=sz, bs=bs, keep_pct=keep_pct) #-> loads the data using the get_data function with the specified batch size, image size, and data percentage.
learn_gen.unfreeze() #-> unfreezes the model layers, allowing all layers to be fine-tuned.
learn_gen.fit_one_cycle(1, pct_start=pct_start, max_lr=slice(1e-7,1e-4))
learn_gen.save(pre_gen_name)


##############################
# 192
##############################
bs=11
sz=192
keep_pct=0.50
learn_gen.data = get_data(sz=sz, bs=bs, keep_pct=keep_pct)
learn_gen.unfreeze()
learn_gen.fit_one_cycle(1, pct_start=pct_start, max_lr=slice(5e-8,5e-5))
learn_gen.save(pre_gen_name)


# Repeatable GAN Cycle
# NOTE :
# Best results so far have been based on repeating the cycle below a few times (about 5-8?), until diminishing returns are hit (no improvement in image quality). Each time you repeat the cycle, you want to increment that old_checkpoint_num by 1 so that new check points don't overwrite the old.
old_checkpoint_num = 0
checkpoint_num = old_checkpoint_num + 1
gen_old_checkpoint_name = gen_name + '_' + str(old_checkpoint_num)
gen_new_checkpoint_name = gen_name + '_' + str(checkpoint_num)
crit_old_checkpoint_name = crit_name + '_' + str(old_checkpoint_num)
crit_new_checkpoint_name= crit_name + '_' + str(checkpoint_num)

# Save Generated Images
bs=8
sz=192

learn_gen = gen_learner_deep(data=data_gen, gen_loss=FeatureLoss(), nf_factor=nf_factor).load(gen_old_checkpoint_name, with_opt=False)
save_gen_images()


# Pretrain Critic
# Only need full pretraining of critic when starting from scratch. Otherwise, just finetune!

if old_checkpoint_num == 0: #_> This condition checks if the old_checkpoint_num is 0, indicating that the training is starting from scratch.
    bs=32
    sz=128
    learn_gen=None
    gc.collect()
    data_crit = get_crit_data([name_gen, 'test'], bs=bs, sz=sz)
    data_crit.show_batch(rows=3, ds_type=DatasetType.Train, imgsize=3)
    learn_critic = colorize_crit_learner(data=data_crit, nf=256)
    learn_critic.callback_fns.append(partial(LearnerTensorboardWriter, base_dir=TENSORBOARD_PATH, name='CriticPre'))
    learn_critic.fit_one_cycle(6, 1e-3) #-> Trains the critic model for six cycles with a learning rate of 1e-3.
    learn_critic.save(crit_old_checkpoint_name)




bs=16
sz=192
data_crit = get_crit_data([name_gen, 'test'], bs=bs, sz=sz)
data_crit.show_batch(rows=3, ds_type=DatasetType.Train, imgsize=3)
learn_critic = colorize_crit_learner(data=data_crit, nf=256).load(crit_old_checkpoint_name, with_opt=False)
learn_critic.callback_fns.append(partial(LearnerTensorboardWriter, base_dir=TENSORBOARD_PATH, name='CriticPre'))
learn_critic.fit_one_cycle(4, 1e-4)
learn_critic.save(crit_new_checkpoint_name)


# GAN
learn_crit=None
learn_gen=None
gc.collect()

lr=1e-5
sz=192
bs=9

data_crit = get_crit_data([name_gen, 'test'], bs=bs, sz=sz) #-> Loads the data for training the critic model

learn_crit = colorize_crit_learner(data=data_crit, nf=256).load(crit_new_checkpoint_name, with_opt=False) #-> Initializes the critic learner with the loaded data and network factor (nf=256). It loads weights from the crit_new_checkpoint_name without loading the optimizer state (with_opt=False).
learn_gen = gen_learner_deep(data=data_gen, gen_loss=FeatureLoss(), nf_factor=nf_factor).load(gen_old_checkpoint_name, with_opt=False) #->  Initializes the generator learner with the loaded data, loss function (FeatureLoss), and network factor (nf_factor). It loads weights from the gen_old_checkpoint_name without loading the optimizer state.

switcher = partial(AdaptiveGANSwitcher, critic_thresh=0.65)
learn = GANLearner.from_learners(learn_gen, learn_crit, weights_gen=(1.0,2.0), show_img=False, switcher=switcher,
                                opt_func=partial(optim.Adam, betas=(0.,0.9)), wd=1e-3) #-> wd = weight decay
learn.callback_fns.append(partial(GANDiscriminativeLR, mult_lr=5.))
learn.callback_fns.append(partial(GANTensorboardWriter, base_dir=TENSORBOARD_PATH, name='GanLearner', visual_iters=100))
learn.callback_fns.append(partial(GANSaveCallback, learn_gen=learn_gen, filename=gen_new_checkpoint_name, save_iters=100))

# Instructions:
# Find the checkpoint just before where glitches start to be introduced. This is all very new so you may need to play around with just how far you go here with keep_pct.
learn.data = get_data(sz=sz, bs=bs, keep_pct=0.03)
learn_gen.freeze_to(-1) #-> This freezes all layers of the generator model up to the last layer (-1), which means that only the final layers of the generator will be trainable.
learn.fit(1,lr)