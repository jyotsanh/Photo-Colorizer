# DeOldify: A Review and Implementation of an Automatic Colorization Method.

## ABOUT

* IPOL website: TO_COMPLETE
* Version number: TO_COMPLETE
* Date: April 2022
* Author    : Antoine Salmona <antoine.salmona@parisdescartes.fr>, Lucía Bouza <lucia.bouza-hegeurte@u-paris.fr>
* Copyright : (C) 2022 IPOL Image Processing On Line http://www.ipol.im/
* Licence   : GPL v3+, see GPLv3.txt

## OVERVIEW

This source code provides a PyTorch implementation of a simplified but effective version of DeOldify without dependence on the Fast.ai framework.

### Contents

* main.py: Main Script to parse arguments and call train, predict or colorize videos
* model.py: Module implementing the training, predict and colorize video functions
* unet.py: Module implementing the network
* layers.py: Module implementing particular layers needed by the network
* loss.py: Module implementing Feature Loss
* data.py: Module implementing functions to load and transform training data
* utils.py: Useful functions for initializations
* run.sh: script to run the IPOL demo
* requirements.txt: package requirements
* resources folder: Containing some tests images and a video colored

## USER GUIDE

The code as is runs in Python 3.8.10 with the following dependencies:

### Dependencies

Detailed versions on requirements.txt:

* [PyTorch](http://pytorch.org/)
* [Torchvision](https://pytorch.org/vision/stable/index.html)
* [scikit-learn](https://scikit-learn.org/stable/)
* [OpenCV](https://pypi.org/project/opencv-python/)

### Usage

#### 1. Testing

If you want to colorize an image using the pretrained model found you can execute:

```

python3 main.py \
    --pretrained= <path to the model> \
    --saturation_value=2.0 \
    --render_factor=12 \   
    --img= "Path to your image"
```

If you want to colorize a video using the pretrained model found you can execute:

```

python3 main.py \
    --pretrained= <path to the model> \
    --saturation_value=2.0 \
    --render_factor=12 \   
    --video= "Path to your video or folder with videos"
```

**NOTES**

* Model have been trained with spectral normalization
* The default render_factor is 12, but it is possible this value not be the best for your image.
* The resulting image will be called "Colorized.jpeg" and will be in the same directory as main.py

#### 2. Training

The network is trained with four epochs of Imagenet (https://image-net.org/challenges/LSVRC/2012/index.php). During  the two first epochs, the training images are down-sampled to  $ 64 \times 64 $ pixels. During the third epoch, they are down-sampled only to $ 128 \times 128 $ pixels, and $ 192 \times 192 $ pixels for the last epoch.

epoch 1:

```
python main.py --train=True --train_data="Path to train data" --normalize=True --img_size=64 --batch_size=88 --max_lr=1e-3 --middle=0.8 --spectral=True  
```

epoch 2:

```
python3 main.py --train=True --train_data="Path to train data" --normalize=True --img_size=64 --batch_size=88 --max_lr=3e-4 --middle=1e-8 --pretrained=./training/epoch_0.pth --spectral=True
```

epoch 3:

```
python main.py --train=True --train_data="Path to train data" --normalize=True --img_size=128 --batch_size=20 --max_lr=1e-4 --middle=1e-8 --pretrained=./training/epoch_0.pth --spectral=True
```

epoch 4:

```
python main.py --train=True --train_data="Path to train data" --normalize=True --img_size=192 --batch_size=8 --max_lr=5e-5 --middle=1e-8 --pretrained=./training/epoch_0.pth --percent=0.5 --spectral=True
```

## ABOUT THIS FILE

Copyright 2022 IPOL Image Processing On Line http://www.ipol.im/

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
