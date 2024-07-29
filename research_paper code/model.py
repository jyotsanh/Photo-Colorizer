#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Module implementing the training and predict functions

Copyright (C) 2022, antoine.salmona@parisdescartes.fr, lucia.bouza-heguerte@u-paris.fr

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>
"""

import os
import torch
import torch.optim as optim
import torch.nn.functional as F
from loss import FeatureLoss
from torch.utils.data import DataLoader
from utils import init_network_
from torch.autograd import Variable
import numpy as np
from tqdm import tqdm
import warnings
from PIL import Image
import PIL
import cv2
from pathlib import PurePath, Path

optimizers_dict = {
    'adadelta': optim.Adadelta,
    'adagrad': optim.Adagrad,
    'adam': optim.Adam,
    'adamw': optim.AdamW,
    'sparseadam': optim.SparseAdam,
    'adamax': optim.Adamax,
    'asgd': optim.ASGD,
    'lbfgs': optim.LBFGS,
    'rmsprop': optim.RMSprop,
    'rprop': optim.Rprop,
    'sgd': optim.SGD,
}

loss_dict = {
    'l1': F.l1_loss,
    'mse': F.mse_loss,
    'smooth_l1': F.smooth_l1_loss,
    'bce': F.binary_cross_entropy,
    'featureloss': FeatureLoss,
}


class Model:
    """Main class for training and prediction."""
    IMAGENET_MEAN = torch.Tensor([0.485, 0.456, 0.406])
    IMAGENET_STD = torch.Tensor([0.229, 0.224, 0.225])


    def __init__(self, model, optimizer='adamw', criterion='featureloss',
                 optimizer_params=dict(), loss_params=dict()):
        """
        Args: 
            model (nn.Module): network to be trained or used for prediction.
            optimizer (string): optimizer for training (see optimizers_dict).
            criterion (string): loss function (see loss_dict).
            n_gpu (int): number of gpus available, if 0 set model on cpu.
            optimizer_params (dict): dictionary of parameters for optimizer.
            loss_params (dict): dictionary of parameters for loss.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model
        self.pretrained = self.model.pretrained
        self.model = self.model.to(self.device)

        self.optimizer = optimizers_dict[optimizer](filter(lambda p: p.requires_grad, self.model.parameters()), **optimizer_params)
        self.criterion = loss_dict[criterion](**loss_params)
        self.criterion = self.criterion.to(self.device)



    def fit(self, data, n_epochs, batch_size, val_data=None, shuffle=True, resume_training=False, log_dir='training',
            save_dir='save', percent=1.0, max_lr=1e-3, div_factor=25, momentum_range=(0.95, 0.85), middle=0.8,
            alpha_popping=30,
            freq_save=1000):
        """Train the model using one cycle policy defined in https://arxiv.org/abs/1803.09820.
        
        Args: 
            data (Dataset): training datas.
            n_epochs (int): number of epochs.
            batch_size (int): size of batchs.
            val_data (Dataset): validation datas (if not none).
            shuffle (boolean): if True change the order of training datas at each epochs. 
            resume training (boolean): if True resume an interrupted training (model is stored at log_dir/ckpt.pth).
            log_dir (string): folder for storing models  
            save_dir (string): folder for saving test images
            percent (float): percent of dataset used for training. 
            max_lr (float): maximum learning rate for one cycle policy.
            div_factor (int): factor of division of maximum learning rate for starting learning rate.
            momentum_range (tuple): higher and lower bounds for momentum during one cycle.
            middle (float): percent of iterations of one epoch for the first phase of the cycle.
            alpha_popping (int): set level of noise for reducing popping effect.
            freq_save (int): set frequency for saving model and training images (0 means never)
        """
        # Load data
        train_loader = DataLoader(data, batch_size=batch_size, shuffle=shuffle, pin_memory=True, drop_last=True)
        if val_data is not None:
            val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False, pin_memory=True, drop_last=True)
        # Create dir if necessary and log
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        # Resume training or start a new
        if resume_training:
            resumef = os.path.join(log_dir, 'ckpt.pth')
            if os.path.isfile(resumef):
                checkpoint = torch.load(resumef)
                print("> Resuming previous training")
                if self.device=="cuda" and torch.cuda.device_count() > 1:
                    self.model.module.load_state_dict(checkpoint['state_dict'])
                else:
                    self.model.load_state_dict(checkpoint['state_dict'])
                self.optimizer.load_state_dict(checkpoint['optimizer'])
                lr = self.optimizer.param_groups[0]['lr']
                training_params = checkpoint['training_params']
                start_epoch = training_params['epoch']
                step = training_params['step']
                if step == len(train_loader) - 1:
                    start_epoch = start_epoch + 1
                    step = 0
                resume_training = False
            else:
                raise Exception("Couldn't resume training with checkpoint {}". \
                                format(resumef))
        else:
            start_epoch = 0
            step = 0
            training_params = {}
            lr = max_lr / div_factor
            momentum = momentum_range[0]
            self.optimizer.param_groups[0]['lr'] = lr
            self.optimizer.param_groups[0]['momentum'] = momentum
            training_params['step'] = 0
            training_params['current_lr'] = lr
            training_params['momentum'] = momentum
            training_params['epoch'] = 0
            if not self.pretrained:
                init_network_(self.model)

        # Training loop
        for epoch in range(start_epoch, n_epochs):
            self.model.train()
            loop = tqdm(train_loader, total=int(percent * len(train_loader)),
                        unit_scale=batch_size, unit='images', position=step)
            for inputs, ground_truths in loop:
                inputs, ground_truths = Variable(inputs).to(self.device), Variable(ground_truths).to(self.device)
                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                # Block for saving images during training
                if freq_save != 0 and step % freq_save == 0:
                    printer = outputs[0].detach().cpu().permute(1, 2, 0)
                    printer = printer.mul(other=Model.IMAGENET_STD).add(other=Model.IMAGENET_MEAN)
                    printer = printer.mul(255).numpy()
                    Image.fromarray(printer.astype(np.uint8)).save(save_dir + '/img_step_%d.jpg' % (step))
                with warnings.catch_warnings():  # Ignore a useless warning
                    warnings.simplefilter("ignore")
                    loss = self.criterion(outputs, ground_truths)
                loss.backward()
                self.optimizer.step()
                loop.set_description('Epoch {}/{}'.format(epoch + 1, n_epochs))
                train_loss = loss.item()
                loop.set_postfix(loss=train_loss, lr=lr)
                step += 1
                if step >= int(percent * len(train_loader)) - 1:
                    step = 0
                    break
                # Phase 1 1Cycle policy
                elif step < int(middle * int(percent * len(train_loader))):
                    lr += (max_lr / (middle * int(percent * len(train_loader)))) * (div_factor - 1) / div_factor
                    momentum -= (momentum_range[0] - momentum_range[1]) / int(percent * len(train_loader))
                    self.optimizer.param_groups[0]['lr'] = lr
                    self.optimizer.param_groups[0]['momentum'] = momentum
                # Phase 2 1Cycle policy
                else:
                    T_curr = step - int(middle * int(percent * len(train_loader)))
                    T_max = int((1-middle)*int(percent * len(train_loader)))
                    lr = max_lr / div_factor + (1. / 2) * (max_lr - max_lr / div_factor) * (
                                1 + np.cos(T_curr * np.pi / T_max))
                    momentum = momentum_range[0] \
                               + (1. / 2) * (momentum_range[1] - momentum_range[0]) * (
                                           1 + np.cos(T_curr * np.pi / T_max))

                training_params['step'] = step
                training_params['current_lr'] = lr
                training_params['momentum'] = momentum
                training_params['epoch'] = epoch

                save_dict = {'state_dict': self.model.state_dict(), 'training_params': training_params}

                # Save checkpoint
                if freq_save != 0 and step % freq_save == 0:
                    torch.save(save_dict, os.path.join(log_dir, 'ckpt.pth'))
            torch.save(save_dict, os.path.join(log_dir, 'epoch_' + str(epoch) + '.pth'))
            
            # Validate after each epoch
            if val_data is not None:
                val_loss = list()
                self.model.eval()
                for inputs, ground_truth in val_loader:
                        inputs, ground_truths = Variable(inputs).to(self.device), Variable(ground_truths).to(self.device)
                outputs = self.model(inputs)
                with warnings.catch_warnings():  # ignore a useless warning
                    warnings.simplefilter("ignore")
                    loss = self.criterion(outputs, ground_truths)
                    val_loss.append(loss.item())
                loop.set_postfix(train_loss=train_loss, val_loss=np.mean(val_loss))


    def predict(self, x, render_factor, saturation_value, post_process=True, normalize=True):
        """predict a colored image from a black and white image. 
        
        Args:
            x (Image): the image to be colorized (not necessarily black and white).
            render_factor (int): set the size of the input tensor for inference
            saturation_value (float): set the value of saturation of colours. A value of 1.0 don't saturate colors. 
            post_process (boolean): if True applies post processing (shady trick).
            normalize (boolean): if True applies ImageNet normalization
        Returns:
            out (Image): the colorized image.
        """
        self.model.eval()
        if post_process:
            Y = cv2.cvtColor(np.array(x), cv2.COLOR_BGR2YUV)[:, :, 0]
        x = x.convert('LA').convert('RGB')
        w, h = x.size
        x = x.resize((16 * render_factor, 16 * render_factor), resample=Image.BILINEAR)
        x = torch.from_numpy(np.array(x, dtype=np.float32)).div_(255)
        if normalize:
            x = x.sub(other=Model.IMAGENET_MEAN).div(other=Model.IMAGENET_STD)
        x = x.unsqueeze_(0).permute(0, 3, 1, 2)
        x = x.to(self.device)
        out = self.model(x)
        out = out.permute(0, 2, 3, 1).squeeze_(0)
        out = out.cpu()
        if normalize:
            out = out.mul(other=Model.IMAGENET_STD).add(other=Model.IMAGENET_MEAN)
        out = torch.clamp(out,0,1)
        out = out.mul_(255)
        out = out.detach().numpy().astype(np.uint8)
        out = Image.fromarray(out)
        out = out.resize((w, h), resample=Image.BILINEAR)
        if post_process:
            out = cv2.cvtColor(np.array(out), cv2.COLOR_BGR2YUV)
            out[:, :, 0] = Y
            out = cv2.cvtColor(out, cv2.COLOR_YUV2BGR)
            out = Image.fromarray(out)
        converter = PIL.ImageEnhance.Color(out)
        return converter.enhance(saturation_value)


    def colorize_videos(self, file, render_factor, saturation_value, post_process=True, normalize=True, fps=23.976):
        """predict a colored video from a black and white video.  
        
        Args:
            file (video): the video to be colorized (not necessarily black and white).
            render_factor (int): set the size of the input tensor for inference
            saturation_value (float): set the value of saturation of colours. A value of 1.0 don't saturate colors. 
            post_process (boolean): if True applies post processing (shady trick).
            normalize (boolean): if True applies ImageNet normalization
        Returns:
            out (Image): the colorized image.
        """
        frame_list = list()
        cap = cv2.VideoCapture(file)
        while(1):
            ret, frame = cap.read()
            frame_list.append(frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
                cap.release()
                cv2.destroyAllWindows()
                break
        path = PurePath(file)
        process_list = list()
        for frame in tqdm(frame_list[:-1], desc='Processing ' + path.name, unit='frame'):
            processed_frame = self.predict(PIL.Image.fromarray(frame), render_factor = render_factor, saturation_value =saturation_value, post_process= post_process, normalize=normalize)
            process_list.append(processed_frame)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        height, width, channel = frame_list[0].shape
        result_path = Path('.') / (path.stem + '_colored.mov')
        video = cv2.VideoWriter(str(result_path), fourcc, fps, (width, height), True)
        process_list[2].save('test_video.jpeg','JPEG')
        for frame in process_list:
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
            video.write(frame)
