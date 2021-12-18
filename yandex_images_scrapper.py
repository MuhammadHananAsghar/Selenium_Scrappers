from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from time import sleep
import requests 
import shutil
import pickle
import uuid
import os
import json


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


bot_path = "drivers/geckodriver"
bot = webdriver.Firefox(options=options, executable_path=bot_path)
bot.get("https://yandex.com/images/search?text=surprised%20child%20face")
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

divs = bot.find_elements_by_class_name("serp-item")
_images = []
for div in divs:
    _json = div.get_attribute("data-bem")
    _json = json.loads(_json)
    _json = _json['serp-item']
    _urls = _json['preview'][0]
    _images.append(_urls['url'])


def download(url):
    name = url.split("/")[-1]
    print(f"Downloading: {name}")
    response = requests.get(url)
    with open(f"/home/zerosec/Desktop/Selenium/data/surprised/{name}", 'wb') as handle:
        handle.write(response.content)

with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(download, _images) #urls=[list of url]
    
bot.quit()
    
