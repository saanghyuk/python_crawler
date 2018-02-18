import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd

import re
#
# options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# options.add_argument("disabl®e-infobars")
# options.add_argument("--disable-extensions")
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# browser = webdriver.Chrome('../../../chromedriver', chrome_options=options)
browser=webdriver.Chrome('../../../chromedriver')
browser.set_window_size(2000, 1500)


data = {'provider': [],'title': [], 'start_date': [], 'end_date':[], "place":[], "artist":[], "url":[], "imageUrl":[]}
#티켓 링크
time.sleep(0.1)

browser.get("http://www.ticketlink.co.kr/concert/concert")

elem= browser.find_element_by_tag_name("body")
i=0
while i<10:
    i+=1
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)

bs=BeautifulSoup(browser.page_source, "html5lib")
#ticket_list=bs.findAll("ul", {"class":{"goods_list"}})
ticket_list=bs.find("div", {"class":{"bottom_area total_wrap"}}).findAll("li")


date_list=[]
date_lists=[]
for ticket in ticket_list:
    print("ticket Link!!! ok!!")
    data['provider'].append('ticket_link')
    data['title'].append(ticket.find("strong", {"class":{"elp"}}).text)
    date_list.append(ticket.find("dd").text)
    data['place'].append(ticket.find("dd").next_sibling.next_sibling.text)
    data['artist'].append("Null")
    data['url'].append("www.ticketlink.co.kr"+ticket.find("a").attrs['href'])
    data['imageUrl'].append(ticket.find("p").img['src'].replace("//", ""))

for i in date_list:
    date_lists.append(i.split('~'))
print(date_lists)

for i in date_lists:
     data['start_date'].append(i[0].replace(".", "-").strip())
     data['end_date'].append(i[1].replace(".", "-").strip())

print(len(data['start_date']))
print(len(data['end_date']))