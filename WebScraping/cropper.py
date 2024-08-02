from PIL import Image
import os

def crop_footer(image_path, save_path, footer_height):
    # Open an image file
    with Image.open(image_path) as img:
        # Get dimensions
        width, height = img.size

        # Define the cropping box (left, upper, right, lower)
        box = (0, 0, width, height - footer_height)

        # Crop the image
        cropped_img = img.crop(box)

        # Save the cropped image
        cropped_img.save(save_path)

def crop_footers_in_directory(input_directory, output_directory, footer_height):
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Loop over all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_directory, filename)
            save_path = os.path.join(output_directory, filename)

            crop_footer(image_path, save_path, footer_height)
            print(f"Cropped {filename} and saved to {save_path}")

# Usage
input_directory = './downloaded_images'
output_directory = './data'
footer_height = 100  # Adjust this value as needed

crop_footers_in_directory(input_directory, output_directory, footer_height)
