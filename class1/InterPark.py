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


browser=webdriver.Chrome('../../../chromedriver')
html = urlopen("http://ticket.interpark.com/TPGoodsList.asp?Ca=Liv")
bs0bj = BeautifulSoup(html.read(), "html.parser")


data = {'platform': ['Interpark Ticket'],'title': [], 'date': [], "place":[], "artist":[], "url":[]}
link_list = bs0bj.findAll("span", {"class": "fw_bold"})
# data['title']=bs0bj.find("span", {"class": "fw_bold"}).text
# data['place']=bs0bj.find("td", {"class": "Rkdate"}).text
# data['date']=bs0bj.find("")r

a=0
for link in link_list:
    selenium_link='http://ticketpark.com'+link.a['href']
    browser.get(selenium_link)
    detailPageSource=BeautifulSoup(browser.page_source, 'lxml')
    data['title'].append(detailPageSource.find("span",{"id": "IDGoodsName"}).text)
    data['url'].append(selenium_link)
    # data['place'].append(detailPageSource.find("ul", {"class":"info_Lst"}).li.next_sibling.next_sibling.dd.text)
    data['date'].append(detailPageSource.find("dt", text="기간").next_sibling.text.replace("\n관람시간 보기\n", ""))
    # print(detailPageSource.find("ul", {"class": "info_Lst"}).li.next_sibling.next_sibling.next_sibling)
    # data['date'].append(detailPageSource.find("span", text=re.compile("20[0-9]+\.[0-9]+\.[0-9]+")).text)
    data['place'].append(detailPageSource.find("dt", text="장소").next_sibling.text)

    browser.maximize_window()
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
        artists = ""
        i = 0
        for artist in artistList:
            if i == len(artistList) - 1:
                artists += artist.find("a").text
            else:
                artists += artist.find("a").text + ", "
                i = i + 1
        data['artist'].append(artists)
        browser.switch_to_default_content()

        #그니깐 지금 아티스트가 과도하게 많아 왜? None이 필요 시앙으로 많이 들어가고 있따는 거지
    else:
        data['artist'].append("None")

browser.close()


print(len(data['artist']))
print("\n")
print(len(data["title"]))
print("\n")
print(len((data['date'])))
print("\n")
print(len(data['place']))
print(("\n"))
print(len((data['url'])))

try:
    df = pd.DataFrame(data, columns=["title", "date", "place", "artist", "url"])
    try:
        df.to_csv("Interpark.csv", encoding='utf-8-sig')

    except:
        pass

except:
    pass
print(data)


#df=pd.DataFrame(data, columns=["title", "date", "place", "artist", "url"])

#df.to_csv("Interpark.csv", encoding='utf-8-sig')
    # print(a)
    # artistBs=BeautifulSoup(browser.page_source, 'lxml')
    # artistList=artistBs.findAll("ul", {"class": "Text"})
    # print(artistBs)
    # for artist in artistList:
    #     print(artist.h3.a.text)

    #browser.find_element_by_xpath("/html/body/div[9]/div[2]/div[1]/map/area").click()
    # browser.find_element_by_xpath("//*[@id='TabA']/div[2]/ul[1]/li[4]/dl/dd/span[2]/a").click()