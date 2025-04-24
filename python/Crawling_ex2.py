from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# 웹 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 크롤링할 웹 페이지 URL
url = 'https://ko.aliexpress.com/item/1005006404381520.html?spm=a2g0o.order_list.order_list_main.4.d975140ftRvLSF&gatewayAdapt=glo2kor'

# 웹 페이지 로드
driver.get(url)

# 페이지 소스 가져오기
html = driver.page_source

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(html, 'html.parser')

# 특정 클래스 이름을 가진 모든 <div> 요소 가져오기
divs = soup.find_all('div', class_='list--itemReview--xQUhO78')
for div in divs:
    print(div.text)

# 웹 드라이버 종료
driver.quit()

# selenium을 써야하는 이유는 현재 알리 웹 페이지가 동적 페이지라서 그런듯.
# beautifulSoup를 써야하는 이유는 HTML 문서 파싱 후 원하는 데이터를 쉽게 가져오기 위해서임ㅇㅇ. => 이거 안쓰면 좀 코드가 난잡해질 가능성이 존재함.