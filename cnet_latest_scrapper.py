from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

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

DRIVER = "drivers/geckodriver"
bot = webdriver.Firefox(options=options, executable_path=DRIVER)

KEYWORD = "tech"
PAGES = 2000
data = []
for idx in range(1, 2001):
    try:
        bot.get(f"https://www.cnet.com/{KEYWORD}/{idx}/")
        sleep(0.2)
        LATEST_HEADLINES = bot.find_elements_by_class_name("c-universalLatest_item")
        for heading in LATEST_HEADLINES:
            text = heading.find_element_by_tag_name("h3").text
            data.append({
                "keyword": KEYWORD,
                "headline": text
            })
    except:
        pass
        
with open(f"{KEYWORD}.json", "w") as file:
    file.write(data)
    
bot.close()

