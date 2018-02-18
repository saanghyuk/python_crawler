import time
from selenium import webdriver

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=options, executable_path='../../../chromedriver')


import re


# browser=webdriver.PhantomJS('/Users/sanghyuk/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs', service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
browser.set_window_size(2000, 1500)

#print(browser.get_window_size())
html = urlopen("http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GroupCode=17011581")
browser.get("http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GroupCode=17011581")
temporaryObj = BeautifulSoup(browser.page_source, 'lxml')

if temporaryObj.find("div", {"class": "capchaLayer"}):
    browser.find_element_by_xpath('/html/body/div[9]/div[2]/div[1]/map/area').click()
else:
    pass

if temporaryObj.find("dt", text="출연"):
    try:
        browser.find_element_by_xpath("//*[@id='TabA']/div[2]/ul[1]/li[4]/dl/dd/span[2]/a").click()
    except NoSuchElementException:
        browser.find_element_by_xpath("//*[@id='TabA']/div[2]/ul[1]/li[3]/dl/dd/span[2]/a").click()


    time.sleep(0.1)
    browser.switch_to_frame(browser.find_element_by_id("ifrTabC"))
    artistPageSource = BeautifulSoup(browser.page_source, "lxml")
    artistList = artistPageSource.findAll("dd", {"class", "inFo"})
    artists=""
    i=0
    for artist in artistList:
        if i == len(artistList) - 1:
            artists += artist.find("a").text
        else:
            artists += artist.find("a").text + ", "
        i = i + 1
browser.switch_to_default_content()


print(artists)

browser.quit()