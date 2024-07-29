#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Module implementing functions to load and transform training data

Copyright (C) 2022, antoine.salmona@parisdescartes.fr, lucia.bouza-heguerte@u-paris.fr

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>
"""

import torch
import torch.utils.data as data
from pathlib import Path
from PIL import Image
import numpy as np
from tqdm import tqdm 


class Dataset(data.Dataset):
    """Class for loading data for training."""
    IMAGENET_MEAN = torch.Tensor([0.485, 0.456, 0.406])
    IMAGENET_STD = torch.Tensor([0.229, 0.224, 0.225])
    
    
    def __init__(self,file,img_size=192,normalize=False):
        """
        Args:
            file (string): Repertory where the datas are.
            img_size (int): size of images for training.
            normalize (boolean): if True normalize images using imagenet statistics
        """
        super().__init__()
        self.img_files = list()
        for file in  tqdm(Path(file).glob('**/*.JPEG'),unit='files'): #tqdm plots a progress bar
            self.img_files.append(file)           
        self.size = len(self.img_files)
        self.img_size = img_size
        self.normalize = normalize


    def __getitem__(self,index):
        index = index % self.size
        img = Image.open(self.img_files[index]).convert('RGB') 
        img = img.resize((self.img_size,self.img_size), resample= Image.BILINEAR) #resize to a square image
        img_bw = img.convert('LA').convert('RGB') #image in black and white#channel first
        img = torch.from_numpy(np.array(img,dtype=np.float32)).div_(255) #scale image between 0 and 1
        
        img_bw = torch.from_numpy(np.array(img_bw,dtype=np.float32)).div_(255) #scale image between 0 and 1 

        if self.normalize:
            img = img.sub_(other=Dataset.IMAGENET_MEAN).div_(other=Dataset.IMAGENET_STD) #normalize image using imagenet statistics            
            img_bw = img_bw.sub_(other=Dataset.IMAGENET_MEAN).div_(other=Dataset.IMAGENET_STD)
        img_bw = img_bw.permute(2,0,1) #channels first
        img = img.permute(2,0,1) #channels first
        return img_bw,img
    def __len__(self):
        return self.size
