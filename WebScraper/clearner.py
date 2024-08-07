import os
from PIL import Image
import numpy as np

def is_valid_image(image_path):
    try:
        with Image.open(image_path) as img:
            img_array = np.array(img)
            if img_array.size == 0:
                return False
        return True
    except Exception as e:
        # If there's an error opening or processing the image, it's considered invalid
        return False

def check_and_delete_images(folder_path):
    invalid_images = []
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            if not is_valid_image(file_path):
                invalid_images.append(filename)
                os.remove(file_path)  # Delete the invalid image
    
    return invalid_images

# Specify the path to your images folder
images_folder = "./images"

# Check and delete invalid images
invalid_images = check_and_delete_images(images_folder)

# Print deleted image names
if invalid_images:
    print("Deleted invalid images:")
    for img_name in invalid_images:
        print(img_name)
else:
    print("All images are valid.")
