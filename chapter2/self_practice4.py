from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen("http://www.pythonscraping.com/pages/page3.html")
bs0bj=BeautifulSoup(html, "html.parser")

for child in bs0bj.find("table", {"id": "giftList"}).children:
    print(child)
