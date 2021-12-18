from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import concurrent.futures
from time import sleep
import requests 
import shutil
import pickle
import uuid
import os


options = Options()
options.add_argument("Cache-Control=no-cache")
options.add_argument("--no-sandbox")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-web-security")
options.add_argument("--ignore-certificate-errors")
options.page_load_strategy = 'none'
options.add_argument("--ignore-certificate-errors-spki-list")
options.add_argument("--ignore-ssl-errors")


input = input("Enter Query : ")
bot_path = "drivers/geckodriver"
bot = webdriver.Firefox(options=options, executable_path=bot_path)
bot.get(f"https://unsplash.com/s/photos/{input}")
sleep(1)

print("Bot is Scrolling")
SCROLL_PAUSE_TIME = 4
# Get scroll height
last_height = bot.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)
			    # Calculate new scroll height and compare with last scroll height
    new_height = bot.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

anchors_images = bot.find_elements_by_class_name("image-result__link")

image_urls = []
images = bot.find_elements_by_class_name("_2UpQX")
for image in images:
    image_urls.append(image.get_attribute("src"))
    
directory = "/data/lion/"
def download(url):
    try:
      filename = str(uuid.uuid4())
      r = requests.get(url, stream = True)
      if r.status_code == 200:
        r.raw.decode_content = True
        file = directory+filename+".jpg"
        with open(file,'wb') as f:
          shutil.copyfileobj(r.raw, f)
          print(f'{len(os.listdir(directory))} : Image sucessfully Downloaded: ',filename)
      else:
          print('Image Couldn\'t be retreived')
    except:
      pass
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(download, image_urls)
  

bot.quit()