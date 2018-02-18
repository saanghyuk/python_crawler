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
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

import re

#티켓 링크
browser = webdriver.PhantomJS('/Users/sanghyuk/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
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


data = {'platform': [],'title': [], 'date': [], "place":[], "artist":[], "url":[]}
for ticket in ticket_list:
    data['platform'].append('Ticket Link')
    data['title'].append(ticket.find("strong", {"class":{"elp"}}).text)
    data['date'].append(ticket.find("dd").text)
    data['place'].append(ticket.find("dd").next_sibling.next_sibling.text)
    data['artist'].append("Null")
    data['url'].append("www.ticketlink.co.kr"+ticket.find("a").attrs['href'])



#인터 파크 티켓
html = urlopen("http://ticket.interpark.com/TPGoodsList.asp?Ca=Liv")
bs0bj = BeautifulSoup(html.read(), "html.parser")
link_list = bs0bj.findAll("span", {"class": "fw_bold"})

browser.get('http://ticket.interpark.com/TPGoodsList.asp?Ca=Liv')
for link in link_list:
    print(link.a['href'])
    selenium_link='http://ticket.interpark.com'+link.a['href']
    browser.get(selenium_link)
    detailPageSource=BeautifulSoup(browser.page_source, 'lxml')
    data['platform'].append('InterPark Ticket')
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

#멜론 티켓
browser.get("http://ticket.melon.com/region/index.htm")
elem = browser.find_element_by_tag_name("body")
i=0
while i<15:
    i+=1
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)

bs = BeautifulSoup(browser.page_source, "html5lib")
ticket_list = bs.find("ul", {"class": {"list_main_concert tapping on"}}).findAll("li")

for ticket in ticket_list:
    try:
        url="http://ticket.melon.com"+ticket.a["href"]
        browser.get(url)
        html = urlopen(url)
        bs0bj=BeautifulSoup(html.read(), "html.parser")
        data['platform'].append('Melon Ticket')
        data['title'].append(bs0bj.find("p", {"class":"tit"}).text)
        data['date'].append(bs0bj.find("dd", {"id":"periodInfo"}).text)
        data['place'].append(bs0bj.find("span", {"class":"place"}).text.replace("\xa0", ""))
        data['url'].append(url)

        if bs0bj.find("ul", {"class": "list_artist"}):
            if bs0bj.select_one("a[href*=javascript:openPopArtistList()]"):
                browser.find_element_by_xpath("//*[@id='conts']/div/div[3]/div[1]/div[1]/div/a").click()
                browser.switch_to_window(browser.window_handles[-1])
                time.sleep(3)
                detailBs=BeautifulSoup(browser.page_source, 'lxml')
                artistList=detailBs.find("ul", {"class":{"list_guest"}}).findAll("strong")
                artists=""
                i=0
                for artist in artistList:
                    if i==len(artistList)-1:
                        artists += artist.text
                    else:
                        artists += artist.text +", "
                    i=i+1
                data['artist'].append(artists)
                browser.close()
                browser.switch_to_window(browser.window_handles[0])
            else:
                artistList=bs0bj.findAll("strong", {"class": "singer"})
                artists=""
                i=0
                for artist in artistList:
                    if i==len(artistList)-1:
                        artists += artist.text
                    else:
                        artists+=artist.text +", "
                        i=+1
                data['artist'].append(artists)
        else:
            data['artist'].append("Null")
    except:
        pass


print(len(data['platform']))
print(len(data['title']))
print(len(data['date']))
print(len(data['place']))
print(len(data['artist']))
print(len(data['url']))
print(len(data['imageUrl']))

df = pd.DataFrame(data, columns=["platform", "title", "date", "place", "artist", "url"])
df.to_csv("Total Ticket List.csv", encoding='utf-8-sig')





