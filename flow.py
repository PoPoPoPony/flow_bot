from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import choice
from grab import Grab, GrabError
import pandas as pd
import requests
from bs4 import BeautifulSoup
def driver_settings() :
	options = webdriver.ChromeOptions()

	agent = [
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.30 Safari/537.36',
		"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    	"Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    	"Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    	"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    	"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    	"Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
	]
	options.add_argument("user-agent = {}".format(choice(agent)))

	prefs = {"profile.managed_default_content_settings.images": 2}
	options.add_experimental_option('prefs' , prefs)

	return options


def proxy_settings(ip):
	proxy = Proxy()
	proxy.proxy_type = ProxyType.MANUAL
	proxy.httpProxy=ip

	capabilities = webdriver.DesiredCapabilities.CHROME
	proxy.add_to_capabilities(capabilities)

	return capabilities
	driver = webdriver.Chrome(desired_capabilities=capabilities)

def get_ip_lst_1() -> list:
	driver = webdriver.Chrome(options=driver_settings(), executable_path='./chromedriver')

	base_url = 'https://www.us-proxy.org'
	ip_lst = []

	driver.get(base_url)
	show_ip_btn = driver.find_element_by_xpath('/html/body/section[1]/div/div[1]/ul/li[6]/a')
	show_ip_btn.click()

	ip_text = driver.find_element_by_xpath('//*[@id="raw"]/div/div/div[2]/textarea').get_attribute('value')
	driver.quit()

	for i in ip_text.split("\n"):
		ip_lst.append(i)

	ip_lst = ip_lst[4:-1]

	return ip_lst


def check_ip(ip_lst, song_id) -> list:
	print(len(ip_lst))
	g = Grab()

	for i in ip_lst:
		g.setup(proxy=i, proxy_type='http', connect_timeout=20, timeout=20)
		try:
			g.go('google.com')
			print("vaild proxy {}".format(i))
			try:
				add_flow(i, song_id)
			except Exception as e:
				print("faild")

		except GrabError as e:
			print("faild to use proxy {}".format(i))



def add_flow(proxy, song_id):
	driver = webdriver.Chrome(options=driver_settings(), executable_path='./chromedriver', desired_capabilities=proxy_settings(proxy))
	target_url = 'https://streetvoice.com/HandyLee/songs/' + str(song_id)
	# target_url = 'https://streetvoice.com/Woody217088/songs/' + str(song_id)

	driver.get(target_url)
	driver.maximize_window()

	if wait_element(driver):
		sleep(3)
		count_elem =  driver.find_element_by_id('countup-play')
		before_count = count_elem.text

		print("before play count : {}".format(before_count))

		after_count = 0
		flag = 0
		result=True

		while after_count <= int(before_count) and flag < 1:
			if result:
				play_btn = driver.find_element_by_xpath('//*[@id="inside_box"]/div[2]/div/div[2]/div/div[2]/ul/li[4]/button')
				play_btn.click()

				sleep(1)

				scrollbar = driver.find_elements_by_class_name('progress')[0]

				action = ActionChains(driver)
				action.drag_and_drop_by_offset(scrollbar, 150, 0).release().perform()

				sleep(8)

				driver.refresh()
				result = wait_element(driver)
				sleep(3)
				count_elem =  driver.find_element_by_id('countup-play')

				after_count = int(count_elem.text)
				flag+=1



		print("after play count : {}".format(after_count))
		driver.quit()


def wait_element(driver):
	try:
		count_elem = WebDriverWait(driver, 20).until(
			EC.presence_of_element_located((By.ID, 'countup-play'))
		)
		scroll_elem = WebDriverWait(driver, 20).until(
			EC.presence_of_element_located((By.CLASS_NAME, 'progress'))
		)
		return True

	except Exception as e:
		driver.quit()
		print("faild to load page")
		return False
