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
#
options = webdriver.ChromeOptions()
#options.binary_location = '../../../chromedriver'
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
browser = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
#browser =webdriver.Firefox('/usr/bin/firefox')
#browser = webdriver.Chrome('../../../chromedriver', chrome_options=options)
browser.set_window_size(2000, 1500)
#멜론 티켓

data = {'platform': [],'title': [], 'date': [], "place":[], "artist":[], "url":[], "imageUrl":[]}


browser.get("http://ticket.melon.com/region/index.htm")
elem= browser.find_element_by_tag_name("body")
no_of_pagedowns=20
while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1



bs = BeautifulSoup(browser.page_source, "html5lib")
print(bs)
ticket_list = bs.find("ul", {"class": {"list_main_concert tapping on"}}).findAll("li")

for ticket in ticket_list:
    try:
        print("Melon Ticket!!! ok!!")
        url="http://ticket.melon.com"+ticket.a["href"]
        browser.get(url)
        html = urlopen(url)
        bs0bj=BeautifulSoup(html.read(), "html.parser")
        data['platform'].append('Melon Ticket')
        data['title'].append(bs0bj.find("p", {"class":"tit"}).text)
        data['date'].append(bs0bj.find("dd", {"id":"periodInfo"}).text)
        data['place'].append(bs0bj.find("span", {"class":"place"}).text.replace("\xa0", ""))
        data['url'].append(url)
        data['imageUrl'].append(bs0bj.find("div", {"class": "box_consert_thumb thumb_180x254"}).img['src'])
        print(data['imageUrl'])

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


browser.close()
print(data)
df = pd.DataFrame(data, columns=["platform", "title", "date", "place", "artist", "url", "imageUrl"])
df.to_csv("Total Ticket List.csv", encoding='utf-8-sig')
print(df)





