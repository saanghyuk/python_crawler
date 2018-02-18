from urllib.request import urlopen
#url에 있는 페이지를 오픈 하겠다.
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html=urlopen(url)
    except HTTPError as e:
        return None

    try:
        bs0bj = BeautifulSoup(html.read(), "html.parser")
        title=bs0bj.body.h1
    except AttributeError as e:
        #Attribute Error -> href, class, id
        return None
    return title

title=getTitle("http://www.pythonscraping.com/pagesadslkfa")
if title==None:
    print("Title could not be found")
else:
    print(title)
