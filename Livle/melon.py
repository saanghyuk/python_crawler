import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd




data = {'platform': [],'title': [], 'start_date': [], 'end_date':[], "place":[], "artist":[], "url":[], "imageUrl":[]}

browser=webdriver.Chrome('../../../chromedriver')
browser.set_window_size(2000, 1500)
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
date_list=[]
date_lists=[]
for ticket in ticket_list:
    try:
        print("Melon Ticket!!!")
        url="http://ticket.melon.com"+ticket.a["href"]
        browser.get(url)
        html = urlopen(url)
        bs0bj=BeautifulSoup(html.read(), "html.parser")
        data['platform'].append('Melon Ticket')
        data['title'].append(bs0bj.find("p", {"class":"tit"}).text)
        date_list.append(bs0bj.find("dd", {"id":"periodInfo"}).text)

        try:
            data['place'].append(bs0bj.find("span", {"class":"place"}).text.replace("\xa0", " "))
        except:
            data['place'].append("Null")
        data['url'].append(url)
        data['imageUrl'].append(bs0bj.find("div", {"class": "box_consert_thumb thumb_180x254"}).img['src'])

        print(bs0bj.find("p", {"class":"tit"}).text)
        print(bs0bj.find("p", {"class":"tit"}).text, " 의 url : ", url)
        print("imageurl : ", bs0bj.find("div", {"class": "box_consert_thumb thumb_180x254"}).img['src'])
        if bs0bj.find("ul", {"class": "list_artist"}):
            if bs0bj.select_one("a[href*=javascript:openPopArtistList()]"):
                try:
                    browser.find_element_by_xpath("//*[@id='conts']/div/div[3]/div[1]/div[1]/div/a").click()
                except:
                    browser.find_element_by_xpath("//*[@id='conts']/div/div[4]/div[1]/div[1]/div/a").click()
                browser.switch_to_window(browser.window_handles[-1])
                time.sleep(3)
                detailBs=BeautifulSoup(browser.page_source, 'lxml')
                artistList=detailBs.find("div", {"class":{"txt_name"}}).findAll("strong")
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
                artistList = bs0bj.findAll("ul", {"class": "list_artist"})
                artists = ""
                i = 0
                for artist in artistList:
                    if i == len(artistList) - 1:
                        artists += artist.li.a.text.strip()
                    else:
                        artists += artist.li.a.text.strip() + ", "
                        i = +1
                data['artist'].append(artists)
        else:
            data['artist'].append("Null")
    except:
        pass

for i in date_list:
    date_lists.append(i.split('-'))
for i in date_lists:
    data['start_date'].append(i[0].strip())
    data['end_date'].append(i[1].strip())

browser.close()

print(len(data['platform']))
print(len(data['title']))
print(len(data['start_date']))
print(len(data['end_date']))
print(len(data['place']))
print(len(data['artist']))
print(len(data['url']))
print(len(data['imageUrl']))
