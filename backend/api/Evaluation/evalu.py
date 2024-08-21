import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_squared_error

# Function to ensure images are resized to the same dimensions
def resize_image(image, size=(192, 192)):
    if image is None:
        return None
    return cv2.resize(image, size)

# Function to calculate metrics
def calculate_metrics(img_true, img_pred):
    mse_value = mean_squared_error(img_true.ravel(), img_pred.ravel())
    psnr_value = cv2.PSNR(img_true, img_pred)
    ssim_value, _ = ssim(img_true, img_pred, win_size=5, channel_axis=2, full=True)
    return mse_value, psnr_value, ssim_value

# Define the folders
original_folder = 'G:/Photo-Colorizer/backend/api/Evaluation/Original Image'
finetune_folder = 'G:/Photo-Colorizer/backend/api/Evaluation/FineTune'
pretrained_folder = 'G:/Photo-Colorizer/backend/api/Evaluation/PreTrained'

# Initialize lists to store metrics
mse_finetune, psnr_finetune, ssim_finetune = [], [], []
mse_pretrained, psnr_pretrained, ssim_pretrained = [], [], []

# Loop through each file in the original folder
for filename in os.listdir(original_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        # Load and resize the original image
        original_path = os.path.join(original_folder, filename)
        original_image = resize_image(cv2.imread(original_path))

        if original_image is None:
            print(f"Warning: Could not load original image: {original_path}")
            continue

        # Load and resize the fine-tuned model's output
        finetune_path = os.path.join(finetune_folder, filename)
        finetune_image = resize_image(cv2.imread(finetune_path))

        if finetune_image is None:
            print(f"Warning: Could not load fine-tuned image: {finetune_path}")
            continue

        # Load and resize the pre-trained model's output
        pretrained_path = os.path.join(pretrained_folder, filename)
        pretrained_image = resize_image(cv2.imread(pretrained_path))

        if pretrained_image is None:
            print(f"Warning: Could not load pre-trained image: {pretrained_path}")
            continue

        # Calculate metrics for fine-tuned model
        mse_f, psnr_f, ssim_f = calculate_metrics(original_image, finetune_image)
        mse_finetune.append(mse_f)
        psnr_finetune.append(psnr_f)
        ssim_finetune.append(ssim_f)

        # Calculate metrics for pre-trained model
        mse_p, psnr_p, ssim_p = calculate_metrics(original_image, pretrained_image)
        mse_pretrained.append(mse_p)
        psnr_pretrained.append(psnr_p)
        ssim_pretrained.append(ssim_p)

# Calculate average metrics
avg_mse_finetune = np.mean(mse_finetune)
avg_psnr_finetune = np.mean(psnr_finetune)
avg_ssim_finetune = np.mean(ssim_finetune)

avg_mse_pretrained = np.mean(mse_pretrained)
avg_psnr_pretrained = np.mean(psnr_pretrained)
avg_ssim_pretrained = np.mean(ssim_pretrained)

# Print the results
print("Fine-tuned Model: MSE: {:.4f}, PSNR: {:.4f}, SSIM: {:.4f}".format(avg_mse_finetune, avg_psnr_finetune, avg_ssim_finetune))
print("Pre-trained Model: MSE: {:.4f}, PSNR: {:.4f}, SSIM: {:.4f}".format(avg_mse_pretrained, avg_psnr_pretrained, avg_ssim_pretrained))
