from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen("http://www.pythonscraping.com/pages/page3.html")
bs0bj = BeautifulSoup(html, "html.parser")

#next_sibling의 의미, next_siblings와 sibling의 차이
#previous_siblings와 previous_sibling

print(bs0bj.find("table", {"id":"giftList"}).tr.next_sibling)
for sibling in bs0bj.find("table", {"id":"giftList"}).tr.next_sibling:
    print(sibling)

for sibling in bs0bj.find("table", {"id":"giftList"}).tr.previous_siblings:
    print(sibling)

print(bs0bj.find("img", {"src":"../img/gifts/img1.jpg"}).parent.previous_sibling.get_text())