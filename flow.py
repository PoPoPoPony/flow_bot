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
import os
from random import choice

def driver_settings() :
	options = webdriver.ChromeOptions()
	agent = [
		"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
		"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
		"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
		"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
		"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
		"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
		"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
		"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
		"Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
		"Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
		"Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
		"Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
		"Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
		"Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
	]

	options.add_argument("User-Agent={}".format(choice(agent)))

	referer='https://accounts.pixiv.net/loginlang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
	options.add_argument("Referer = {}".format(referer))

	prefs = {
		"profile.managed_default_content_settings.images": 2,
		'profile.default_content_settings.popups': 0,
		"download.prompt_for_download": False,
		"download.directory_upgrade": True,
		'download.default_directory': get_current_directory(),
	}
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


def get_current_directory():
	temp = os.getcwd().replace('\\', '%', 1)
	temp = temp.replace('\\', '/')
	directory = temp.replace('%', '\\')
	directory += " "

	return directory


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

	url = 'https://spys.one/en/free-proxy-list/'

	driver.get(url)
	sleep(2)

	try:
		select_elem = WebDriverWait(driver, 20).until(
			EC.presence_of_element_located((By.ID, 'xpp'))
		)

	except Exception as e:
		print("failed to proxy list")
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


def get_ip_lst_3() -> list:
	driver = webdriver.Chrome(options=driver_settings(), executable_path='./chromedriver')

	base_url = 'https://www.proxy-list.download/'

	connect_type = ["HTTPS", "SOCKS4", "SOCKS5"]

	for i in connect_type:
		url = base_url + i
		driver.get(url)
		sleep(5)

		driver.execute_script("dllst()")

		sleep(3)

		try:
			os.rename(get_current_directory().strip() + "/Proxy List.txt", get_current_directory().strip() + '/' + i + ".txt")

		except Exception as e:
			print("failed to change file name")
			exit(0)

	driver.quit()

	ip_lst = []

	for i in connect_type:
		df = pd.read_table(i + ".txt", sep='\n', header=None)
		# ip_lst.extend(df.to_list())
		df = df.iloc[:, 0]
		ip_lst.extend(df.to_list())

		if os.path.exists(i + ".txt"):
			os.remove(i + ".txt")
			print("success remove " + i + ".txt")
		else:
			print(i + ".txt does not exist")

	return ip_lst


def get_ip_lst_4(max_page) -> list:
	driver = webdriver.Chrome(options=driver_settings(), executable_path='./chromedriver')

	ip_lst = []
	base_url = 'http://free-proxy.cz/en/proxylist/main/'

	for i in range(1, max_page+1):
		url = base_url + str(i)
		driver.get(url)

		try:
			show_ip_btn = WebDriverWait(driver, 20).until(
				EC.presence_of_element_located((By.ID, 'clickexport'))
			)

		except Exception as e:
			print("failed to load show_ip_btn")
			exit(0)

		show_ip_btn = driver.find_element_by_id('clickexport')
		show_ip_btn.click()

		try:
			proxy_table = WebDriverWait(driver, 20).until(
				EC.presence_of_element_located((By.ID, 'zkzk'))
			)

		except Exception as e:
			print("failed to load proxy table")
			exit(0)

		proxy_table = driver.find_element_by_id('zkzk').text
		sleep(5)

		for j in proxy_table.split("\n"):
			ip_lst.append(j)

	driver.quit()

	return ip_lst

def check_ip(ip_lst, song_id) -> list:
	print("got {} proxies".format(len(ip_lst)))
	g = Grab()

	for i in ip_lst:
		g.setup(proxy=i, proxy_type='http', connect_timeout=15, timeout=15)
		try:
			g.go('google.com')
			print("vaild proxy {}".format(i))
			try:
				add_flow(i, song_id)
			except Exception as e:
				print("failed")

		except GrabError as e:
			print("failed to use proxy {}".format(i))


def add_flow(proxy, song_id):
	driver = webdriver.Chrome(options=driver_settings(), executable_path='./chromedriver', desired_capabilities=proxy_settings(proxy))
	target_url = 'https://streetvoice.com/hey08/songs/' + str(song_id)
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
		print("failed to load page")
		return False
