from selenium import webdriver
import requests
from random import choice
import pandas as pd
from time import sleep
import socket

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
	options.add_argument("user-agent = {}".format(agent[0]))

	prefs = {"profile.managed_default_content_settings.images": 2}
	options.add_experimental_option('prefs' , prefs)

	return options


def get_ip_lst():
	driver = webdriver.Chrome(options=driver_settings(), executable_path='./chromedriver')

	base_url = 'https://www.us-proxy.org'
	ip_lst = []

	driver.get(base_url)
	show_ip_btn = driver.find_element_by_xpath('/html/body/section[1]/div/div[1]/ul/li[6]/a')
	show_ip_btn.click()

	ip_text = driver.find_element_by_xpath('//*[@id="raw"]/div/div/div[2]/textarea').get_attribute('value')
	driver.close()

	for i in ip_text.split("\n"):
		ip_lst.append(i)

	ip_lst = ip_lst[4:-1]

	print(ip_lst)













get_ip_lst()








def add_flow(song_id):
	driver = webdriver.chrome()
	target_url = 'https://streetvoice.com/Woody217088/songs/' + song_id + '/'
