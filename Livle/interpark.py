import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd

browser=webdriver.Chrome('../../../chromedriver')
browser.set_window_size(2000, 1500)

data = {'platform': [],'title': [], 'start_date': [], 'end_date': [], "place":[], "artist":[], "url":[], "imageUrl":[]}


#인터 파크 티켓
html = urlopen("http://ticket.interpark.com/TPGoodsList.asp?Ca=Liv")
bs0bj = BeautifulSoup(html.read(), "html.parser")
link_list = bs0bj.findAll("span", {"class": "fw_bold"})

date_list=[]
date_lists=[] #이 두개 날짜 슬라이스 용

browser.get('http://ticket.interpark.com/TPGoodsList.asp?Ca=Liv')
for link in link_list:
    print(link.a['href'])
    selenium_link='http://ticket.interpark.com'+link.a['href']
    browser.get(selenium_link)
    detailPageSource=BeautifulSoup(browser.page_source, 'lxml')
    print("Inter Park!!! ok!!")
    data['platform'].append('InterPark Ticket')
    data['title'].append(detailPageSource.find("span",{"id": "IDGoodsName"}).text)
    data['url'].append(selenium_link)
    # data['place'].append(detailPageSource.find("ul", {"class":"info_Lst"}).li.next_sibling.next_sibling.dd.text)
    # print(detailPageSource.find("ul", {"class": "info_Lst"}).li.next_sibling.next_sibling.next_sibling)
    # data['date'].append(detailPageSource.find("span", text=re.compile("20[0-9]+\.[0-9]+\.[0-9]+")).text)
    data['place'].append(detailPageSource.find("dt", text="장소").next_sibling.text)
    data['imageUrl'].append(detailPageSource.find("div", {"class": "poster"}).img['src'])
    date_list.append(detailPageSource.find("dt", text="기간").next_sibling.text.replace("\n관람시간 보기\n", ""))

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
                artists += artist.find("a").text.strip()
            else:
                artists += artist.find("a").text.strip() + ", "
                i = i + 1
        data['artist'].append(artists)#
        browser.switch_to_default_content()
        #그니깐 지금 아티스트가 과도하게 많아 왜? None이 필요 시앙으로 많이 들어가고 있따는 거지
    else:
        data['artist'].append("Null")

for a in date_list:
        if "~" in a:
            b=a.split('~')
            data['start_date'].append(b[0].strip())
            data['end_date'].append(b[1].strip())
        else:
            data['start_date'].append(a.strip())
            data['end_date'].append(a.strip())


print(len(data['platform']))
print(len(data['title']))
print(len(data['start_date']))
print(len(data['end_date']))
print(len(data['place']))
print(len(data['artist']))
print(len(data['url']))
print(len(data['imageUrl']))