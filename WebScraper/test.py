import os

def rename_images(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Filter out non-image files (you can customize this based on your needs)
    image_files = [file for file in files if file.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Sort the files to maintain a consistent order (optional)
    image_files.sort()
    
    # Rename the files
    for index, file_name in enumerate(image_files):
        new_name = f"imagev1_{index}.jpg"
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed {file_name} to {new_name}")

# Specify the path to the temples folder
temples_folder_path = "./temples"

# Ensure the folder exists
if os.path.exists(temples_folder_path):
    rename_images(temples_folder_path)
else:
    print(f"The folder {temples_folder_path} does not exist.")
