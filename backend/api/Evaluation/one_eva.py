import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_squared_error

# Function to ensure images are resized to the same dimensions
def resize_image(image, size=(192, 192)):
    if image is None:
        return None
    return cv2.resize(image, size)  # Resize the image to the same dimensions

# Function to calculate metrics
def calculate_metrics(img_true, img_pred):
    mse_value = mean_squared_error(img_true.ravel(), img_pred.ravel())
    psnr_value = cv2.PSNR(img_true, img_pred)
    ssim_value, _ = ssim(img_true, img_pred, win_size=5, channel_axis=2, full=True)
    return mse_value, psnr_value, ssim_value

# Define the paths for a single image
original_image_path = 'G:\\Photo-Colorizer\\backend\\api\\Evaluation\\Original Image\\test_image54.jpg'
finetune_image_path = 'G:\\Photo-Colorizer\\backend\\api\\Evaluation\\FineTune\\ArtisticModel_gen_3\\test_image54.jpg'
pretrained_image_path = 'G:\\Photo-Colorizer\\backend\\api\\Evaluation\\PreTrained\\try1\\test_image54.jpg'




# Load and resize the original image
original_image = cv2.imread(original_image_path)
original_image = resize_image(original_image)

if original_image is None:
    print(f"Original image not found: {original_image_path}")
else:
    # Load and resize the fine-tuned model's output
    finetune_image = cv2.imread(finetune_image_path)
    finetune_image = resize_image(finetune_image)

    if finetune_image is None:
        print(f"Fine-tuned image not found: {finetune_image_path}")
    else:
        # Load and resize the pre-trained model's output
        pretrained_image = cv2.imread(pretrained_image_path)
        pretrained_image = resize_image(pretrained_image)

        if pretrained_image is None:
            print(f"Pre-trained image not found: {pretrained_image_path}")
        else:
            # Calculate metrics for fine-tuned model
            mse_f, psnr_f, ssim_f = calculate_metrics(original_image, finetune_image)
            print("Fine-tuned Model: MSE: {:.4f}, PSNR: {:.4f}, SSIM: {:.4f}".format(mse_f, psnr_f, ssim_f))

            # Calculate metrics for pre-trained model
            mse_p, psnr_p, ssim_p = calculate_metrics(original_image, pretrained_image)
            print("Pre-trained Model: MSE: {:.4f}, PSNR: {:.4f}, SSIM: {:.4f}".format(mse_p, psnr_p, ssim_p))
