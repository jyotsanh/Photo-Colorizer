import torch

# Path to the model file
Fine_tunedpath = './models/fineTuned.pth'
Pretrained_path = './models/ColorizeArtistic_gen.pth'

# Load the model
model = torch.load(Pretrained_path)
fineTune = torch.load(Fine_tunedpath)
# Print the keys
print(model.keys())
print(fineTune.keys())
print("---------------------")

print(model['model'])
print(fineTune['model'])