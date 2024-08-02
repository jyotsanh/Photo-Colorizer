import torch
model_path = './models/ColorizeArtistic_gen.pth'
model_data = torch.load(model_path, map_location='cpu')           
#print(model_data['opt']) # optimizer parameters
print(model_data.keys()) # model parameters
