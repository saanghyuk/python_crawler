from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html=urlopen(url)
    except HTTPError as e:
        return None

    try:
        bs0bj=BeautifulSoup(html.read(), "html.parser")
        body_h1 = bs0bj.body.h1
    except AttributeError as e:
        return None

    return body_h1

title=getTitle("http://pythonscraping.com/pages/page1.html")
if title ==None:
    print("title could not be found")
else:
    print(title)
