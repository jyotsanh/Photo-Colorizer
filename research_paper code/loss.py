#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Module implementing Feature Loss

Copyright (C) 2022, antoine.salmona@parisdescartes.fr, lucia.bouza-heguerte@u-paris.fr

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>
"""

import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F


class FeatureLoss(nn.Module):
    """feature loss using vgg
    inspired from https://cs.stanford.edu/people/jcjohns/papers/eccv16/JohnsonECCV16.pdf.
    
    if f_j(x) is the output of the j^th layer of a vgg network, 
    with f_0 standing for identity, the loss is written:
        L(x,y) =  \sum\limits_{j=0}{3} |f_j(x) - f_j(y)| 
    """

    def __init__(self,model=models.vgg16_bn(pretrained=True),layer_weights=[1,20,70,10],
                 base_loss=F.l1_loss,cuda=True):
        """
        Args:
            model (torchvision.models): the version of vgg (11, 13, 16, or 19) to be used.
            layer_weights (list): list of weights.
            base_loss (torch.functional): the base metric to be used (for instance l1 or mse).
        """
        super().__init__()
        self.features = model.features.eval()
        for param in self.features.parameters():
            param.requires_grad = False     #do not train the network
        self.blocks_idx = [i for i,o in enumerate(self.features.children()) if isinstance(o,nn.MaxPool2d)][2:5]
        self.weights = layer_weights
        self.base_loss = base_loss



    def forward(self,x,y):
        """
        Args:
            x (Tensor): output image of the network.
            y (Tensor): ground truth image.
        Returns:
            loss (Tensor): tensor of dim 1 containing the loss value.
        """
        loss = self.base_loss(x,y)*self.weights[0]
        for i in range(len(self.blocks_idx)):
            features = self.features[0:self.blocks_idx[i]].to(x.device)
            loss += self.base_loss(features(x),features(y))*self.weights[i+1]
            
        return loss
    
