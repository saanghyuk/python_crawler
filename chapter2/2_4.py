from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen("http://pythonscraping.com/pages/page3.html")
bs0bj = BeautifulSoup(html.read(), "html.parser")

images = bs0bj.findAll("img")

#findall은 이터레이터를 리턴함. 텍스트가 될수도 있고, 숫자가 될수도 있고
#id도찾을 수 있음
#이터레이터는 바로 aatrs쓸 수 없음.
#리스트와 엘리먼트는 구분 해야 한다.

for image in images:
    print(image.attrs['src'])
print(image)


#변수 이름 주의하자.
#주의




