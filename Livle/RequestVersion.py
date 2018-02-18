import time
from selenium import webdriver
from urllib.request import urlopen
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
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

data = {'provider': [],'title': [], 'start_date': [], 'end_date':[], "place":[], "artist_info":[], "ticket_url":[], "image_url":[], "key":[]}
data['key']='livlecreatingtempupcoming'

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
    data['provider']='ticket_link'
    data['title']=ticket.find("strong", {"class":{"elp"}}).text
    rawDate=ticket.find("dd").text
    data['place']=ticket.find("dd").next_sibling.next_sibling.text
    data['artist_info']="Null"
    data['ticket_url']="www.ticketlink.co.kr"+ticket.find("a").attrs['href']
    data['image_url']=ticket.find("p").img['src'].replace("//", "")

    rawDateList=rawDate.split('~')
    for i in rawDateList:
        data['start_date'] = i.replace(".", "-").strip()
        data['end_date'] = i.replace(".", "-").strip()
    #post
    requests.post("http://livle.vb9qxcpfgz.ap-northeast-2.elasticbeanstalk.com/insert", data=data)

print(data)

#인터 파크 티켓
html = urlopen("http://ticket.interpark.com/TPGoodsList.asp?Ca=Liv")
bs0bj = BeautifulSoup(html.read(), "html.parser")
link_list = bs0bj.findAll("span", {"class": "fw_bold"})

# date_list=[]
# date_lists=[] #이 두개 날짜 슬라이스 용

browser.get('http://ticket.interpark.com/TPGoodsList.asp?Ca=Liv')
for link in link_list:
    print(link.a['href'])
    selenium_link='http://ticket.interpark.com'+link.a['href']
    browser.get(selenium_link)
    detailPageSource=BeautifulSoup(browser.page_source, 'lxml')
    print("Inter Park!!! ok!!")
    data['provider']='interpark'
    data['title']=detailPageSource.find("span",{"id": "IDGoodsName"}).text
    data['ticket_url']=selenium_link
    # data['place'].append(detailPageSource.find("ul", {"class":"info_Lst"}).li.next_sibling.next_sibling.dd.text)
    # print(detailPageSource.find("ul", {"class": "info_Lst"}).li.next_sibling.next_sibling.next_sibling)
    # data['date'].append(detailPageSource.find("span", text=re.compile("20[0-9]+\.[0-9]+\.[0-9]+")).text)
    data['place']=detailPageSource.find("dt", text="장소").next_sibling.text
    data['image_url']=detailPageSource.find("div", {"class": "poster"}).img['src']
    rawDate=detailPageSource.find("dt", text="기간").next_sibling.text.replace("\n관람시간 보기\n", "")
    if "~" in rawDate:
        rawDateList = rawDate.split('~')
        data['start_date'] = rawDateList[0].replace(".", "-").strip()
        data['end_date'] = rawDateList[1].replace(".", "-").strip()
    else:
        data['start_date']= rawDate.replace(".", "-").strip()
        data['end_date']=data['start_date']

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
        data['artist_info']=artists#
        browser.switch_to_default_content()
        #그니깐 지금 아티스트가 과도하게 많아 왜? None이 필요 시앙으로 많이 들어가고 있따는 거지
    else:
        data['artist_info']="Null"

    requests.post("http://livle.vb9qxcpfgz.ap-northeast-2.elasticbeanstalk.com/insert", data=data)




print(data)
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
        data['provider']='melon'
        data['title']=bs0bj.find("p", {"class":"tit"}).text
        rawDate=bs0bj.find("dd", {"id":"periodInfo"}).text
        rawDateList=rawDate.split('-')
        for i in date_lists:
            data['start_date'] = i[0].replace(".", "-").strip()
            data['end_date'] = i[1].replace(".", "-").strip()

        try:
            data['place']=bs0bj.find("span", {"class":"place"}).text.replace("\xa0", " ")
        except:
            data['place']="Null"
        data['ticket_url']=url
        data['image_url']=bs0bj.find("div", {"class": "box_consert_thumb thumb_180x254"}).img['src']

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
                data['artist_info']=artists
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
                data['artist_info']=artists
        else:
            data['artist_info']="Null"
    except:
        pass

    requests.post("http://livle.vb9qxcpfgz.ap-northeast-2.elasticbeanstalk.com/insert", data=data)

#requests.post("http://livle.vb9qxcpfgz.ap-northeast-2.elasticbeanstalk.com/insert", data=data)


browser.close()

print(data)