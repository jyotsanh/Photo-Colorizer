from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import *
from deoldify.generators import gen_inference_deep
from fastai.vision import *
from fastai.vision.data import ImageImageList
from fastai.vision.learner import unet_learner
from fastai.callbacks.hooks import *
from PIL import Image
import torch

# Set up the device (CPU or GPU)
device.set(device=DeviceId.GPU0)

# Define the dummy DataBunch
def get_dummy_databunch():
    path = Path('./dummy')
    return ImageDataBunch.create_from_ll(
        ImageImageList.from_folder(path, convert_mode='RGB'),
        ImageImageList.from_folder(path, convert_mode='RGB'),
        size=(256, 256),
        bs=1,
    )

# Create the dummy DataBunch
data = get_dummy_databunch()

# Create the learner model
learn = unet_learner(
    data=data,
    arch=models.resnet34,
    loss_func=F.l1_loss,
    norm_type=NormType.Spectral,
    blur=True,
    self_attention=True,
    y_range=(-3.0, 3.0),
    last_cross=True,
    bottle=True,
)

# Load your custom model weights
model_path = './models/fine-tuned.pth'
learn.model.load_state_dict(torch.load(model_path, map_location=lambda storage, loc: storage))

# Define the colorizer object
class ImageColorizer:
    def __init__(self, learn):
        self.learn = learn
    
    def get_transformed_image(self, path, render_factor):
        img = open_image(path).resize(1, 256)
        img = self.learn.predict(img)[0]
        return img

colorizer = ImageColorizer(learn)

# Path to your input image
input_path = './test_images/image.png'

# Colorize the image
result = colorizer.get_transformed_image(path=input_path, render_factor=35)

# Save the colorized image
result.save('colorized_image.jpg')
