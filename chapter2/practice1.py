from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen("http://pythonscraping.com/pages/warandpeace.html")
bs0bj= BeautifulSoup(html.read(), "html.parser")

thePrince = bs0bj.findAll(text="the prince")
print(thePrince)
