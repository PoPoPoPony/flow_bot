from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from time import sleep
from grab import Grab, GrabError
import pandas as pd
from fake_useragent import UserAgent


def driver_settings() :
	options = webdriver.ChromeOptions()
	ua = UserAgent()
	agent = ua.random

	options.add_argument("User-Agent={}".format(agent))

	referer='https://accounts.pixiv.net/loginlang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
	options.add_argument("Referer = {}".format(referer))

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


def get_ip_lst_2() -> list:
	driver = webdriver.Chrome(options=driver_settings(), executable_path='./chromedriver')

	base_url = 'https://spys.one/en/free-proxy-list/'

	driver.get(base_url)
	sleep(2)

	try:
		select_elem = WebDriverWait(driver, 20).until(
			EC.presence_of_element_located((By.ID, 'xpp'))
		)

	except Exception as e:
		print("faild to proxy list")
		exit(0)

	select_elem = Select(driver.find_element_by_id('xpp'))
	select_elem.select_by_value('5')
	sleep(3)
	select_elem = Select(driver.find_element_by_id('xpp'))
	select_elem.select_by_value('5')
	sleep(3)

	table_elem = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[4]/td/table/tbody').get_attribute('innerHTML')
	table_elem = "<table>" + table_elem + "</table>"

	df = pd.read_html(table_elem)[0]

	driver.quit()

	df = df.iloc[:, 0]
	df = df.dropna()
	df = df[2:-1]
	ip_lst = df.to_list()

	for i in range(len(ip_lst)):
		s = ip_lst[i]
		proxy = s.split(".")

		a = proxy.pop(3)
		b = proxy.pop(3)

		a = a[:-8]
		proxy.append(a)
		proxy = ".".join(proxy)

		b = b.split(":")[2]

		proxy = proxy + ":" + b

		ip_lst[i] = proxy

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

	if wait_song_element(driver):
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
				result = wait_song_element(driver)
				sleep(3)
				count_elem =  driver.find_element_by_id('countup-play')

				after_count = int(count_elem.text)
				flag+=1



		print("after play count : {}".format(after_count))
		driver.quit()


def wait_song_element(driver):
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
