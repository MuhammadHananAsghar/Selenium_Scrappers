from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


driver_path = "drivers/chromedriver"
driver = webdriver.Chrome(executable_path=driver_path)
driver.get("https://randomwordgenerator.com/paragraph.php")
sleep(0.2)

paragraph = driver.find_element_by_class_name("support-paragraph")
print(paragraph.text)