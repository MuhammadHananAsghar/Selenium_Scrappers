from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

USERNAME = ""
PASSWORD = ""



class PinterestScrapper:
	def __init__(self, pinterest):
		"""
		Initializing Bot
		"""
		self.driver_path = "drivers/geckodriver"
		self.pinterest = pinterest
		self.login_site = "https://www.pinterest.com/login/"
		self.bot = webdriver.Firefox(options=self.__options(), executable_path=self.driver_path)
		self.__start(self.bot, self.pinterest)


	def __start(self, bot, pinterest):
		"""
		Starting Bot
		"""
		bot.get(self.login_site)
		sleep(2)
		self.__login(bot)
		sleep(2)
		bot.get("https://www.pinterest.com/")
		sleep(2)
		bot.get(pinterest)
		sleep(6)
		self.__scroll(bot)


	def __login(self, bot):
		email = bot.find_element_by_name("id")
		email.clear()
		email.send_keys(USERNAME)
		password = bot.find_element_by_name("password")
		password.clear()
		password.send_keys(PASSWORD)
		button = bot.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div[3]/div/div/div[3]/form/div[5]/button")
		button.click()
		return


	def __scroll(self, driver):
		print("Bot is Scrolling")
		SCROLL_PAUSE_TIME = 2
		# Get scroll height
		last_height = driver.execute_script("return document.body.scrollHeight")
		while True:
			# Scroll down to bottom
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			images = driver.find_elements_by_class_name("hCL")
			for image in images:
				try:
					image = image.get_attribute("src")
					if image.startswith("https://i.pinimg.com/236x/"):
						image = image.replace("https://i.pinimg.com/236x/", "https://i.pinimg.com/originals/")
						print(image)
				except:
					pass
		    # Wait to load page
			sleep(SCROLL_PAUSE_TIME)
			    # Calculate new scroll height and compare with last scroll height
			new_height = driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				break
			last_height = new_height
		return


	def __save(self, __file):
		with open("pinterest.txt", "w") as file:
			file.write(__file)
			file.write("\n")
		file.close()


	def __options(self):
		"""
		Configuring options of the Bot
		"""
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
		return options


tw = PinterestScrapper("https://www.pinterest.com/marysmith25/elon-musk/")
