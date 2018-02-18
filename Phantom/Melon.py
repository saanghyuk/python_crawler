import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
import pandas as pd

import re

options = webdriver.ChromeOptions()
#options.binary_location = '../../../chromedriver'
options.add_argument("start-maximized")
options.add_argument("disabl®e-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
browser = webdriver.Chrome('../../../chromedriver', chrome_options=options)
browser.set_window_size(2000, 1500)

browser.get("http://ticket.melon.com/region/index.htm")
elem= browser.find_element_by_tag_name("body")
#no_of_pagedowns=20
# while no_of_pagedowns:
#     print("페이지 다운")
#     elem.send_keys(Keys.PAGE_DOWN)
#     time.sleep(0.2)
#     no_of_pagedowns-=1
i=0
while i<10:
    i+=1
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)


bs = BeautifulSoup(browser.page_source, "html5lib")
ticket_list = bs.find("ul", {"class":{"list_main_concert tapping on"}}).findAll("li")

data = {'platform':[], 'title': [], 'date': [], "place":[], "artist":[], "url":[], "image": []}

for ticket in ticket_list:
    try:
        url="http://ticket.melon.com"+ticket.a["href"]
        browser.get(url)
        html = urlopen(url)
        bs0bj=BeautifulSoup(html.read(), "html.parser")
        data['platform'].append("Melon Ticket")
        data['title'].append(bs0bj.find("p", {"class":"tit"}).text)
        data['date'].append(bs0bj.find("dd", {"id":"periodInfo"}).text)
        data['place'].append(bs0bj.find("span", {"class":"place"}).text.replace("\xa0", ""))
        data['url'].append(url)
        data['image'].append(bs0bj.find("div", {"class": "box_consert_thumb thumb_180x254"}).img.attrs['src'].text)

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
                        artists += artist.li.a.text
                    else:
                        artists += artist.li.a.text + ", "
                        i = +1
                data['artist'].append(artists)
        else:
            data['artist'].append("None")
    except:
        pass

    break
print(data)



df = pd.DataFrame(data, columns=["platform", "title", "date", "place", "artist", "url", "image"])
df.to_csv("Melon.csv", encoding='utf-8-sig')



        # print(artistList)
        # for artist in artistList:
        #
        # body = browser.find_element_by_tag_name("body")
        # bodyText = body.get_attribute("innerText")
        # print(bodyText)

    # print(bs0bj.find("div", {"class": {"wrap_detail_left_cont"}}).div.div.a)
    # print(bs0bj.find("a", href=True, text="더보기"))
        # browser.find_elements_by_xpath("//*[@id='conts']/div/div[3]/div[1]/div[1]/div/a").click()
        # time.sleep(20)
        # break
    # browser.execute_script("window.history.go(-1)")
#

#셀리늄 브라우져가 여기로 들어와서 더보기를 클릭하던가, 아니면 그냥 뽑던가 해야 하는데, 셀레늄 컨트롤을 못하겠다 그걸 찾아봐야 겠따

# print(data)# BeautifulSoup(html.read(), "html.parser")




#
#for ticket in ticket_list:
#    data['title'].append(ticket.find("strong", {"class":{"elp"}}).text)
#    data['date'].append(ticket.find("dd").text)
#    data['place'].append(ticket.find("dd").next_sibling.next_sibling.text)
#    data['artist'].append
#    data['url'].append("www.ticketlink.co.kr"+ticket.find("a").attrs['href'])

#df=pd.DataFrame(data, columns=["title", "date", "place", "artist", "url"])

#df.to_csv("TicketLink.csv", index=False, encoding='utf-8-sig')