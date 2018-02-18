from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen("http://pythonscraping.com/pages/page1.html")
#이걸 열어서

bs0bj=BeautifulSoup(html.read(), "html.parser")


print(bs0bj.body.div)
#h1이라는 애를 가지고 옴.