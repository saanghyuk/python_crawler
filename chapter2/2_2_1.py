from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen("http://ticket.melon.com/region/index.htm")
bs0bj = BeautifulSoup(html.read(), "html.parser")


print(html)