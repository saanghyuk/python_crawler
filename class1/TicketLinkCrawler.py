#-*- coding:utf-8 -*-
import json
import datetime
import urllib
from urllib.request import urlopen

#from bs4 import BeautifulSoup


ticketPageCount=0

for i in range(1, 10): #???10페이지 까지 있지도않고, 예외처리 한적도 없는데 에러가 안나다니
    html = urlopen("http://www.ticketlink.co.kr/concert/getConcertList?page={}&categoryId=14&frontExposureYn=Y".format(i))
    ticketJsonstr=html.read().decode('utf-8')
    ticketJson=json.loads(ticketJsonstr)
    resultList=ticketJson.get("result").get("result")

    def printPlayInfo(item):
        date =datetime.datetime.fromtimestamp(item["startDate"] / 1e3)
        format_string="%Y-%m-%d"
        date=datetime.datetime.strftime(date, "%Y-%m-%d")
        return "title: %s,|place: %s,|date: %s, |artist: None, |url: ?" % (item["productName"], (item["locationName"]+' '+item["placeName"]).strip(), date)



    #f=open("새 파일.txt", 'w', encoding='utf-8)

    for item in resultList:
        if ticketPageCount==0:
            f = open("ticket.txt", "w", encoding='utf-8')
            printPlayInfo(item)
            data=printPlayInfo(item)
            f.write(data)
            f.write("\n")
            ticketPageCount+=1
            f.close()
        else:
            f = open("ticket.txt", "a", encoding='utf-8')
            printPlayInfo(item)
            data = printPlayInfo(item)
            f.write(data)
            f.write("\n")
f.close()
#print(ticketJson.get("result").get("result")[0])


