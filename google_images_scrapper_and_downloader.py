from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import requests 
import shutil
import uuid


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
bot.get("https://www.google.com.pk/search?q=elon+musk&tbm=isch&ved=2ahUKEwj3p93L2-TwAhU0AmMBHSV4BL0Q2-cCegQIABAA&oq=elon+musk&gs_lcp=CgNpbWcQA1AAWABg7xJoAHAAeACAAQCIAQCSAQCYAQCqAQtnd3Mtd2l6LWltZw&sclient=img&ei=rN2sYPehFrSEjLsPpfCR6As&bih=880&biw=1280&hl=en")
sleep(1)

image_urls = []

print("Bot is Scrolling")
SCROLL_PAUSE_TIME = 2
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
    

div = bot.find_element_by_xpath('//*[@id="islrg"]')
counter_divs = div.find_elements_by_class_name("isv-r")
for _div in counter_divs:
    item = _div.find_elements_by_tag_name("img")
    if len(item) > 0:
        item = item[0]
        image_url = item.get_attribute("src")
        if image_url != None:
            image_urls.append(image_url)
        else:
            pass
    else:
        print("NO URL FOUND")

directory = "data/elon musk/"
print(len(image_urls))
for url in image_urls:   
    try:
        filename = str(uuid.uuid4())
        r = requests.get(url, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            file = directory+filename
            with open(file,'wb') as f:
                shutil.copyfileobj(r.raw, f)
            print('Image sucessfully Downloaded: ',filename)
        else:
            print('Image Couldn\'t be retreived')
    except:
        pass