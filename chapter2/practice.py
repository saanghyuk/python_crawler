

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.r114.com/z/real/m_gu.asp?only=0&m_=5&g_=&type=m&type_m=m&type_g=A&type_cd=03%5E05&addr1=%BC%AD%BF%EF%C6%AF%BA%B0%BD%C3&addr2=%B0%FC%BE%C7%B1%B8&addr3=&fromnavi=1")
bs0bj = BeautifulSoup(html.read(), "html.parser")

nameList=bs0bj.findAll("a", {"class": "blue in_view_link"})

#딕셔너리로 리턴
#print(type(nameList))
#이터레이터 속성을 가지고 있으면 돌려서 뽑을 수 있음.
print("----------nameList------------")
for name in nameList:
    print(name.get_text())