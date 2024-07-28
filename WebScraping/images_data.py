import requests
import os

file_path = './image_urls.txt'
index = 1565
try:
    with open(file_path, 'r') as image_urls:
        for url in image_urls:
            print()
            print(url)
            url = url.strip()
            img_data = requests.get(url).content
            with open(f'downloaded_images/image_{index + 1}.jpg', 'wb') as img_file:
                img_file.write(img_data)
            print(f'Downloaded image {index + 1}')
            index += 1
            
except FileNotFoundError:
    print(f"The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
