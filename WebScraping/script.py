from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

count = 17
options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

for page in range(count, count+8):
    driver.get(f"https://www.shutterstock.com/search/colorful-kathmandu-temple?page={page}")
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    div_elements = driver.find_elements(By.CSS_SELECTOR, 'div[role="img"]')
    for div in div_elements:
        try:
            a_element = div.find_element(By.CSS_SELECTOR, 'a[aria-label]')
            if a_element:  # Ensure the <a> element is found
                aria_label = a_element.get_attribute("aria-label")
                href = a_element.get_attribute("href")
                photo_id = href.split("-")[-1]
                aria_label = aria_label.replace(",", "").replace(".", "")
                aria_label =aria_label.lower()
            
                text_lis = aria_label.split(" ")
                if len(text_lis) >= 14:
                        urls_list = text_lis[:14]
                        print(urls_list)
                        
                else:
                    urls_list = text_lis[1:]
                    print(urls_list)

                half_url = "https://www.shutterstock.com/shutterstock/photos/"
                joined_text = "-".join(urls_list)


                updated_urls = half_url+photo_id+"/display_1500/stock-photo-"+joined_text+"-"+photo_id+".jpg"

                print(updated_urls)
                time.sleep(1)
                with open('./image_urls.txt', 'a') as text_file:
                    text_file.write(updated_urls+ '\n')
            else:
                print("not found")
        except Exception as e:
            print("error")
        
driver.quit()
