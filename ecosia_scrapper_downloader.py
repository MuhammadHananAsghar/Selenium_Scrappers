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
bot.get(f"https://www.ecosia.org/images?q={input}")
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
for a in anchors_images:
    image_urls.append(a.get_attribute("href"))

os.mkdir(f"data/{input}")    
directory = f"data/{input}/"
print(len(image_urls))
with open(directory+f"{input}.txt", "wb") as fp:
    pickle.dump(image_urls, fp)
    
bot.quit()