from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen("http://pythonscraping.com/pages/warandpeace.html")
bs0bj = BeautifulSoup(html.read(), "html.parser")

nameList=bs0bj.findAll("span", {"class":"red"})

#텍스트 출력하는 부분
for name in nameList:
    print(name.get_text())