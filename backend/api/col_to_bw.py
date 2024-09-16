import cv2
import os

# Define the input and output folders
input_folder = './Evaluation/Original Image'
output_folder = './Evaluation/GrayScale'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):  # You can add more image file extensions if needed
        # Construct the full file path
        file_path = os.path.join(input_folder, filename)

        # Read the image
        image = cv2.imread(file_path)

        # Convert the image to grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Resize the grayscale image to 192x192 pixels
        resized_image = cv2.resize(grayscale_image, (192, 192))

        # Save the resized grayscale image in the output folder with the same name as the original
        grayscale_filename = os.path.join(output_folder, filename)
        cv2.imwrite(grayscale_filename, grayscale_image)

print("Processing complete. Resized grayscale images saved in the output folder.")
