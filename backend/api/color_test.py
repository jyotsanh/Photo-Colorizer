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
    def __init__(self,model_name):
        self.model_name = model_name
        pass
    def convert(self,b_w_image_path='./test_images/rose.jpg',url=''):
        colorizer = get_image_colorizer(model_name=self.model_name,artistic=True)
        render_factor = 35  #@param {type: "slider", min: 7, max: 40}
        watermarked = True #@param {type:"boolean"}
        
        image_path = colorizer.plot_transformed_image_from_url(
            url = url,
            path=b_w_image_path,
            render_factor=35, 
            compare=True, 
            watermarked=watermarked
            )
        print(image_path)
        return image_path
        
def WrapperConverter(path,url,model_name):
    
    if path is not None and url == '':
        converter = Converter(model_name)
        return converter.convert(path,url)
    else:
        print('Provide an image url and try again.')
        return False


if __name__ == '__main__':
    models = ['ArtisticModel_gen_0','ArtisticModel_gen_1','ArtisticModel_gen_2','ArtisticModel_gen_3','ArtisticModel_gen_4','ArtisticModel_gen_5','ArtisticModel_gen_6','ArtisticModel_gen_7','ArtisticModel_gen_8']
    for i in range(0,29):
        model_name = f"ArtisticModel_gen_4"
        path = f"G:/Photo-Colorizer/backend/api/Evaluation/GrayScale/test_image{i+1}.jpg"
        url=''
        print(model_name)
        WrapperConverter(path=path,url= url,model_name=model_name)