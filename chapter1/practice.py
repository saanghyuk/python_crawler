from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup

try:
    html=urlopen("http://pythonscraping.com/pages/page1.html")
except HTTPError as e:
    print(e)

else:
    bs0bj=BeautifulSoup(html.read(), "html.parser")
    print(bs0bj)