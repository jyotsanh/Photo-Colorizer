from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib
import base64
import requests
count = 17
options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

driver.get("https://www.google.com/search?sca_esv=e3ff2cacd83f1ace&sca_upv=1&q=boudha+temple+images&udm=2&fbs=AEQNm0A-5VTqs5rweptgTqb6m-Eb3TvVcv4l7eCyod9RtZW9874wvsYjTfpwMQKGHqKPG-IB7j9flyfH28tJSLVuVdcT1tesPpIhTR_8sOQ3FQrQWuC5aA5eChfkgoaHVKBAsrn4doMfEM16y1MBs3qs7RGc0y2rp-Kmv-19eNKPOZAJVCcGcRNDqnnAXYLEf9pKN9hKZYECvymoMntOOuVV2S1Vi3x9gg&sa=X&ved=2ahUKEwjxjuvGpM-HAxWp1TQHHdNDOpUQtKgLegQIEBAB&biw=1920&bih=959&dpr=1")
time.sleep(4)

# Start scrolling down
start_time = time.time()
while time.time() - start_time < 160:
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)  # Small delay to avoid sending too many keys too quickly

time.sleep(7)
# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Example: print the title of the page
print(soup.title.string)
links = soup.find_all("h3",class_="ob5Hkd")
urls_list = []
indx = 780
for i in links:
    
    try:
        image_data = base64.b64decode(i.find("img")['src'][23:])

        # Save the image
        with open(f"./images/output{indx}.jpg", "wb") as file:
            file.write(image_data)
    except:
        print("Error occured base64")
        try:
            response = requests.get(i.find("img")['src'])
            if response.status_code == 200:
                # Save the image
                with open(f"./images/output{indx}.jpg", "wb") as file:
                    file.write(response.content)
                print("Image saved as downloaded_image.jpg")
            else:
                print("Failed to retrieve the image")
        except:
            print(i.find("img")['src'])
            print("Error occured while saving https")
    indx+=1
    
driver.quit()
