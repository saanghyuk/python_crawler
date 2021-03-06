import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime

print(datetime.time())
browser = webdriver.Chrome('../../../chromedriver')
time.sleep(1)

browser.get("http://www.ticketlink.co.kr/concert/concert")

elem= browser.find_element_by_tag_name("body")
no_of_pagedowns=20

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1

bs=BeautifulSoup(browser.page_source, "html5lib")
#ticket_list=bs.findAll("ul", {"class":{"goods_list"}})
ticket_list=bs.find("div", {"class":{"bottom_area total_wrap"}}).findAll("li")


data = {'platform': ['Ticket Link'],'title': [], 'date': [], "place":[], "artist":[], "url":[]}
for ticket in ticket_list:
    data['title'].append(ticket.find("strong", {"class":{"elp"}}).text)
    data['date'].append(ticket.find("dd").text)
    data['place'].append(ticket.find("dd").next_sibling.next_sibling.text)
    data['artist'].append("Null")
    data['url'].append("www.ticketlink.co.kr"+ticket.find("a").attrs['href'])


df=pd.DataFrame(data, columns=["title", "date", "place", "artist", "url"])
df.to_csv("TicketLink.csv", index=False, encoding='utf-8-sig')