#NOTE:  This must be the first call in order to work properly!
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)

import torch

if not torch.cuda.is_available():
    print('GPU not available.')
    
    
import fastai
from deoldify.visualize import *
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")


def main():
    colorizer = get_image_colorizer(artistic=True)


    path_p = './test_images/rose.jpg' #@param {type:"string"}
    render_factor = 35  #@param {type: "slider", min: 7, max: 40}
    watermarked = True #@param {type:"boolean"}

    if path_p is not None and path_p !='':
        image_path = colorizer.plot_transformed_image_from_url(
            url='',
            path=path_p,
            render_factor=render_factor, 
            compare=True, 
            watermarked=watermarked
            )
        print(image_path)
    else:
        print('Provide an image url and try again.')
    
    
class Converter():
    def __init__(self):
        pass
    def convert(self,b_w_image_path='./test_images/rose.jpg'):
        colorizer = get_image_colorizer(artistic=True)
        render_factor = 35  #@param {type: "slider", min: 7, max: 40}
        watermarked = True #@param {type:"boolean"}

        if b_w_image_path is not None and b_w_image_path !='':
            image_path = colorizer.plot_transformed_image_from_url(
                url = 'https://cdn.naturettl.com/wp-content/uploads/2019/06/27085016/black-white-wildlife-photography-2.jpg',
                path=b_w_image_path,
                render_factor=render_factor, 
                compare=True, 
                watermarked=watermarked
                )
            print(image_path)
        else:
            print('Provide an image url and try again.')

if __name__ == '__main__':
    main()