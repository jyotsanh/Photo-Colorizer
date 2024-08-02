#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Main Script to parse arguments and call train or predict 

Copyright (C) 2022, antoine.salmona@parisdescartes.fr, lucia.bouza-heguerte@u-paris.fr

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>

"""

import glob
import torch
from model import Model
from data import Dataset
from unet import Unet
from PIL import Image
import argparse
from torchvision import models
import os

models_dict = {
    'resnet101': models.resnet101(pretrained=True),
    'vgg16': models.vgg16_bn(pretrained=True)
    }


def parse_args():
    parser = argparse.ArgumentParser(description='DeOldify: a Pytorch implementation')
    #general
	
    parser.add_argument('--train',dest='train',help='if True train the model',type=bool,default=False)
    parser.add_argument('--pretrained',dest='pretrained',help='path to pretrained model file',
                        type=str,default=None)  
    parser.add_argument('--normalize',dest='normalize',
                        help='if True normalize data using imagenet statistics',type=bool,default=True)
    parser.add_argument('--n_channels',dest='n_channels',
                        help='if n_channels=3 predict in RGB (old version), else if n_channels=2 predict in YUV and convert (new version)',
                        type=int,default=2)
    parser.add_argument('--backbone', dest='backbone',
                        help='classifier to be used as backbone',type=str,default='resnet101')
    parser.add_argument('--vgg_loss', dest='vgg_loss',
                        help='vgg version to be used for loss',type=str,default='vgg16')
    parser.add_argument('--spectral', dest='spectral',
                        help='if True apply spectral normalization',default=True)

    #inference
    parser.add_argument('--img',dest='img',help='path to input for inference',type=str,default=None)
    parser.add_argument('--video', dest='source_videos', help='file or dir to read and colorize', type=str,default=None)
    parser.add_argument('--render_factor',dest='render_factor',
                        help='set the size of the input for inference',type=int,default=12)
    parser.add_argument('--post_process',dest='post_process',
                        help='if True applies post processing during inference',type=bool,default=True)
    parser.add_argument('--save_file',dest='save_file',
                        help='colorized image file',type=str,default='colorized.jpeg')
    parser.add_argument('--save_gs',dest='save_gs',
                        help='gray-scale image file',type=str,default='gray_scale.jpeg')
    parser.add_argument('--saturation_value',dest='saturation_value',
                        help='saturation parameter',type=float,default=2.0)

    #training
    parser.add_argument('--train_data',dest='train_data',
                        help='Path to training datas',type=str,
                        default='/mnt/data/shared_datasets/imagenet/imagenet/train')
    parser.add_argument('--val_data',dest='val_data',
                        help='Path to validation datas',type=str,
                        default=None)
    parser.add_argument('--img_size',dest='img_size',
                        help='size of training images',type=int,default=192)
    parser.add_argument('--optim',dest='optim',
                        help='optimizer to be used',type=str,default='adamw')
    parser.add_argument('--criterion',dest='criterion',type=str,
                        help='criterion to be used for training',default='featureloss')
    parser.add_argument('--epochs',dest='epochs',type=int,default=1)
    parser.add_argument('--batch_size',dest='batch_size',
                        help='size of batchs',type=int,default=8)
    parser.add_argument('--resume_training',
                        help='if True resume former training (model is stored in log_dir/ckpt.pth)',
                        type=bool,default=False)
    parser.add_argument('--log_dir',dest='log_dir',
                        help='folder of logs of training',type=str,default='training')
    parser.add_argument('--save_dir',dest='save_dir',
                        help='folder for saving training imgs',type=str,default='save')
    parser.add_argument('--max_lr',dest='max_lr',
                        help='maximum learning rate for one cycle policy',
                        type=float,default=1e-3)
    parser.add_argument('--div_factor',dest='div_factor',
                        help='factor of division of maximum learning rate for starting learning rate',
                        type=int,default=25)
    parser.add_argument('--momentum_range',dest='momentum_range',
                        help='higher and lower bounds for momentum during one cycle',
                        type=tuple,default=(0.95,0.85))
    parser.add_argument('--middle',dest='middle',
                        help='percent of iterations of one epoch for the first phase of the cycle',
                        type=float,default=0.8)
    parser.add_argument('--percent',dest='percent',
                        help='percent of dataset used for training',type=float,default=1.0)
    parser.add_argument('--alpha_popping',dest='alpha_popping',
                        help='coeff for noise to reducing popping effect',type=int,default=30)
    parser.add_argument('--freq_save',dest='freq_save',
                        help='set frequency for saving models and training images (0 means never)',type=int,
                        default=10000)
 

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    backbone = models_dict[args.backbone]
    loss_params = dict()
    loss_params['model'] = models_dict[args.vgg_loss]
    
    # Load network
    if args.n_channels ==3:
        y_range=(torch.Tensor([-3.,-3.,-3.]),torch.Tensor([3.,3.,3.]))
        unet = Unet(n_channels=args.n_channels,pretrained=args.pretrained,backbone=backbone,y_range=y_range,spectral=args.spectral)
    else:
        unet = Unet(n_channels=args.n_channels,pretrained=args.pretrained,backbone=backbone,spectral=args.spectral)  

    # Inference 
    if not args.train:
        if args.pretrained is None:
            raise Exception('please provide a pretrained model: --pretrained=path_to_your_model')   
        model = Model(unet)
        # Colorize images
        if args.img is not None:
            x = Image.open(args.img).convert('RGB')
            # Save gray-scale image
            gs = x.convert('LA').convert('RGB')
            gs.save(args.save_gs,'JPEG')
            # Colorize image
            out = model.predict(x,args.render_factor,args.saturation_value,args.post_process,args.normalize)
            out.save(args.save_file,'JPEG')
        # Colorize videos
        elif args.source_videos is not None:
            # Colorize all the videos inside the folder "args.source_videos"
            if os.path.isdir(args.source_videos):
                files = [f for f in glob.glob(args.source_videos + "**/*.mov", recursive=True)]
                files.sort()
                idx = 1
                for f in files:
                    print('Processing file ' + str(idx) + ' / ' + str(len(files)))
                    model.colorize_videos(f,args.render_factor,args.saturation_value,args.post_process,args.normalize)
                    idx += 1
            # Colorize just one video
            else:
                model.colorize_videos(args.source_videos,args.render_factor,args.saturation_value,args.post_process,args.normalize)
        else:
            raise Exception('please provide an input image file or a source video: --img=path_to_your_img or --video=path_to_your_video')
    # Training
    else:
        if args.train:
            if args.train_data is None:
                raise Exception('please provide training datas: --train_data=path_to_your_datas')
            print('loading data')
            data = Dataset(args.train_data,args.img_size,args.normalize)
            model = Model(unet,args.optim,args.criterion,loss_params=loss_params)
            print('starting training')
            model.fit(data,args.epochs,args.batch_size,val_data=args.val_data,
                        resume_training=args.resume_training,log_dir=args.log_dir,
                        save_dir=args.save_dir,max_lr=args.max_lr,div_factor=args.div_factor,
                        momentum_range=args.momentum_range,middle=args.middle,percent=args.percent,
                        alpha_popping=args.alpha_popping,freq_save=args.freq_save)
        
