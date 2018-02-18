from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen("http://pythonscraping.com/pages/page3.html")
bs0bj = BeautifulSoup(html.read(), "html.parser")

images = bs0bj.findAll("img")

for image in images:
    print(image.attrs['src'])
    