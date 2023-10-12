from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time
import os

PATH = 'path/to/chromedriver'

wd = webdriver.Chrome(PATH)

global query
def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    wd.get(url.format(q=query))

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "sFlh5c") #keeps changing so check and update
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

    return image_urls


def download_image(download_path, url, file_name):


    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)

query=input()
t='_'.join(f'{query}'.lower().split(' '))
urls = get_images_from_google(wd, 1, 100) #given 100 images, alter as per your need
targetfolder="path/to/targetfolder"+"/"+t
if not os.path.exists(targetfolder):
    os.makedirs(targetfolder)
for i, url in enumerate(urls):
    download_image(targetfolder+'/', url, t+str(i) + ".jpg")

wd.quit()
