#NOTE:  This must be the first call in order to work properly!
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)

import torch

if not torch.cuda.is_available():
    print('GPU not available.')
    
    
import fastai
from deoldify.visualize import get_image_colorizer
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

class Converter():
    def __init__(self):
        pass
    def convert(self,b_w_image_path='./test_images/rose.jpg',url=''):
        colorizer = get_image_colorizer(artistic=True)
        render_factor = 35  #@param {type: "slider", min: 7, max: 40}
        watermarked = True #@param {type:"boolean"}
        
        image_path = colorizer.plot_transformed_image_from_url(
            url = url,
            path=b_w_image_path,
            render_factor=render_factor, 
            compare=True, 
            watermarked=watermarked
            )
        print(image_path)
        return image_path
        
def WrapperConverter(path,url):
    
    if path is not None and url == '':
        converter = Converter()
        return converter.convert(path,url)
    else:
        print('Provide an image url and try again.')
        return False


if __name__ == '__main__':
    path = "./test_images/image2.png"
    url=''
    WrapperConverter(path=path,url= url)