import torch
model_path = './models/ArtisticModel_gen_0.pth'
model_data = torch.load(model_path, map_location='cpu')           
#print(model_data['opt']) # optimizer parameters
print(model_data.keys()) # model parameters
