from selenium import webdriver
from bs4 import BeautifulSoup

browser=webdriver.Chrome('../../../chromedriver')
browser.get("http://www.airkorea.or.kr/realSearch")
bs=BeautifulSoup(browser.page_source, "html5lib")

print(bs)