
#정규표현식 .?  찾아보기
#a.{1,2} --> 아무거나 하나 또는 두개
#This .{1,2}
#[0-9]
#{2} 이 중괄호가 몇개냐 표시

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html.read(), "html.parser")

images = bsObj.findAll("img", {"src":re.compile("\.\.\/img\/gifts\/img.*\.jpg")})
print(len(images))
for image in images:

        print(type(image))
        print(image)
        #테그 안에
        print(image['src'])  #bs4의 엘리먼트의 태그니깐 기본적으로 접근 할 수 있음.
        print(image.attrs['src'])#테그 안에 있는 모든 attribute를 딕셔너리 형태로 뽑는다.