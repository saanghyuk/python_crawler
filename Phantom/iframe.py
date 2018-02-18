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
import pandas as pd

import re


browser=webdriver.PhantomJS('/Users/sanghyuk/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs', service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
browser.set_window_size(2000, 1500)

#print(browser.get_window_size())
html = urlopen("http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GroupCode=17011581")
browser.get("http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GroupCode=17011581")
temporaryObj = BeautifulSoup(browser.page_source, 'lxml')
print(browser.page_source) #여기까진 잘 나옴

if temporaryObj.find("div", {"class": "capchaLayer"}):
    browser.find_element_by_xpath('/html/body/div[9]/div[2]/div[1]/map/area').click()
    print("hi")#출력
else:
    print("hello")
    pass

if temporaryObj.find("dt", text="출연"):
    print("sanghyuk")#출력
    try:
        browser.find_element_by_xpath("//*[@id='TabA']/div[2]/ul[1]/li[4]/dl/dd/span[2]/a").click()
        print("hahaha")#출력
    except NoSuchElementException:
        browser.find_element_by_xpath("//*[@id='TabA']/div[2]/ul[1]/li[3]/dl/dd/span[2]/a").click()
        print("nanana")

    time.sleep(0.1)
    browser.switch_to_frame(browser.find_element_by_id("ifrTabC"))
    print(browser.page_source) #여기부터 emptry
    artistPageSource = BeautifulSoup(browser.page_source, "lxml")
    artistList = artistPageSource.findAll("dd", {"class", "inFo"})
    print(browser.page_source) #emptry

    # wait = WebDriverWait(browser, 10)
    # wait.until(EC.presence_of_element_located((By.ID, "ifrTabC")))
    # browser.switch_to_frame(browser.find_element_by_id("ifrTabC"))
    # print(browser.execute_script('return document.documentElement.outerHTML'))
    # print("아이프레임 페이지 소스:", browser.page_source)
else:
    print("lalala")
