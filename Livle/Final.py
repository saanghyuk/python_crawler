import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import requests

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


#data = {'provider': [],'title': [], 'start_date': [], 'end_date':[], "place":[], "artist_info":[], "ticket_url":[], "image_url":[], "key":[]}
data = {'provider': [],'title': [], 'start_date': [], 'end_date':[], "place":[], "artist_info":[], "ticket_url":[], "image_url":[]}
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
    data['artist_info'].append("Null")
    data['ticket_url'].append("www.ticketlink.co.kr"+ticket.find("a").attrs['href'])
    data['image_url'].append(ticket.find("p").img['src'].replace("//", ""))
    break
for i in date_list:
    date_lists.append(i.split('~'))
for i in date_lists:
    data['start_date'].append(i[0].replace(".", "-").strip())

    data['end_date'].append(i[1].replace(".", "-").strip())

print(len(data['provider']))
print(len(data['title']))
print(len(data['start_date']))
print(len(data['end_date']))
print(len(data['place']))
print(len(data['artist_info']))
print(len(data['ticket_url']))
print(len(data['image_url']))


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
    data['provider'].append('interpark')
    data['title'].append(detailPageSource.find("span",{"id": "IDGoodsName"}).text)
    data['ticket_url'].append(selenium_link)
    # data['place'].append(detailPageSource.find("ul", {"class":"info_Lst"}).li.next_sibling.next_sibling.dd.text)
    # print(detailPageSource.find("ul", {"class": "info_Lst"}).li.next_sibling.next_sibling.next_sibling)
    # data['date'].append(detailPageSource.find("span", text=re.compile("20[0-9]+\.[0-9]+\.[0-9]+")).text)
    data['place'].append(detailPageSource.find("dt", text="장소").next_sibling.text)
    data['image_url'].append(detailPageSource.find("div", {"class": "poster"}).img['src'])
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
        data['artist_info'].append(artists)#
        browser.switch_to_default_content()
        #그니깐 지금 아티스트가 과도하게 많아 왜? None이 필요 시앙으로 많이 들어가고 있따는 거지
    else:
        data['artist_info'].append("Null")
    break

for a in date_list:
        if "~" in a:
            b=a.split('~')
            data['start_date'].append(b[0].replace(".", "-").strip())
            data['end_date'].append(b[1].replace(".", "-").strip())
        else:
            data['start_date'].append(a.replace(".", "-").strip())
            data['end_date'].append(a.replace(".", "-").strip())


print(len(data['provider']))
print(len(data['title']))
print(len(data['start_date']))
print(len(data['end_date']))
print(len(data['place']))
print(len(data['artist_info']))
print(len(data['ticket_url']))
print(len(data['image_url']))

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
        data['provider'].append('melon')
        data['title'].append(bs0bj.find("p", {"class":"tit"}).text)
        date_list.append(bs0bj.find("dd", {"id":"periodInfo"}).text)

        try:
            data['place'].append(bs0bj.find("span", {"class":"place"}).text.replace("\xa0", " "))
        except:
            data['place'].append("Null")
        data['ticket_url'].append(url)
        data['image_url'].append(bs0bj.find("div", {"class": "box_consert_thumb thumb_180x254"}).img['src'])

        print(bs0bj.find("p", {"class":"tit"}).text)
        print(bs0bj.find("p", {"class":"tit"}).text, " 의 url : ", url)
        print("image_url : ", bs0bj.find("div", {"class": "box_consert_thumb thumb_180x254"}).img['src'])
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
                data['artist_info'].append(artists)
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
                data['artist_info'].append(artists)
        else:
            data['artist_info'].append("Null")
    except:
        pass

    break
for i in date_list:
    date_lists.append(i.split('-'))
for i in date_lists:
    data['start_date'].append(i[0].replace(".", "-").strip())
    data['end_date'].append(i[1].replace(".", "-").strip())

browser.close()

print(len(data['provider']))
print(len(data['title']))
print(len(data['start_date']))
print(len(data['end_date']))
print(len(data['place']))
print(len(data['artist_info']))
print(len(data['ticket_url']))
print(len(data['image_url']))



print(data)



df = pd.DataFrame(data, columns=["provider", "title", "start_date", "end_date", "place", "artist_info", "ticket_url", "image_url"])
df.to_csv("test926-1.csv", encoding='utf-8-sig')

data_request=data
data_request['key']='livlecreatingtempupcoming'
print(data_request)
requests.post("http://livle.vb9qxcpfgz.ap-northeast-2.elasticbeanstalk.com/insert", data=data_request)
