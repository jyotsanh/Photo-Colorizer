import requests
import os

def save_url_image(url, image_number):
    # Format the new image name
    new_image_name = f"./temples/image{image_number}.jpg"
    
    # Fetch the image from the URL
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(new_image_name, 'wb') as file:
            file.write(response.content)
        print(f"Image saved as {new_image_name}")
    else:
        print(f"Failed to retrieve image from URL: {url}")

temples = {
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/basantapur-tower/photos/basantapur-tower{}.jpg":37,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/bagawati-temple/photos/bagawati_temple{}.jpg":47,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/bodnath-stupa/photos/bodnath-stupa{}.jpg":17,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/hariti-mata-temple/photos/hariti-mata_temple{}.jpg":27,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/indrapur-temple/photos/indrapur-temple{}.jpg":19,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/jagannath-temple/photos/jagannath-temple{}.jpg":40,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/kageshvar-temple/photos/kageshvar-temple{}.jpg":15,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/kathesimbhu-stupa/photos/kathesimbhu_stupa{}.jpg":33,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/kavindrapur-sattal/photos/kavindrapur-sattal{}.jpg":24,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/kotilingeshwar-mahadev/photos/kotilingeshwar_mahadev_temple{}.jpg":18,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/lakshmi-narayan-temple/photos/lakshmi-narayan_temple{}.jpg":27,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/maju-dega-temple/photos/maju-dega_temple{}.jpg":22,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/narayana-temple/photos/narayan-temple{}.jpg":32,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/panchmukhi-hanuman-temple/photos/panchmukhi-hanuman_temple{}.jpg":22,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/shiva-parvati-temple/photos/shiva-parvati_temple{}.jpg":56,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/swayambunatha-stupa/photos/swayambhunatha{}.jpg":47,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/taleju-bhawani-temple/photos/taleju-temple_kathmandu{}.jpg":54,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/trailokya-mohan-narayan/photos/trailokya-mohan_temple{}.jpg":31,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/tripureshwar-mahadev-temple/photos/tripureshwor-mahadev_temple{}.jpg":48,
    "https://www.orientalarchitecture.com/gallery/nepal/kathmandu/vamsha-gopal/photos/octagonal-krishna_temple{}.jpg":22
}

# Create the directory if it doesn't exist
if not os.path.exists('./temples'):
    os.makedirs('./temples')

image_number = 1

for key, value in temples.items():
    for i in range(1, value + 1):
        try:
            if i < 10:
                formatted_url = key.format("0" + str(i))
            else:
                formatted_url = key.format(str(i))

            save_url_image(formatted_url, image_number)
            image_number += 1
        except Exception as e:
            print(f"Error occurred: {e}")
            print(formatted_url)
