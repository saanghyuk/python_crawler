#class를 가지고 데이터를 뽑는다.
#css를 쓰기 위해서 class attribute를 쓰는 것.
#attribute의 id 나 class는 대체로 다르다.


from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://ticket.melon.com/region/index.htm")
bs0bj = BeautifulSoup(html.read(), "html.parser")

nameList=bs0bj.findAll("strong", {"class": "tit"})
#딕셔너리로 리턴
#print(type(nameList))
#이터레이터 속성을 가지고 있으면 돌려서 뽑을 수 있음.
print("----------nameList------------")
for name in nameList:
    print(name)