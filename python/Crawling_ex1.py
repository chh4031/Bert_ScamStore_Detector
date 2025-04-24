import requests
from bs4 import BeautifulSoup

# 크롤링할 웹 페이지 URL
url = 'https://ko.aliexpress.com/item/1005006404381520.html?spm=a2g0o.order_list.order_list_main.4.d975140ftRvLSF&gatewayAdapt=glo2kor'

# 웹 페이지 요청
response = requests.get(url)

# 요청이 성공했는지 확인
if response.status_code == 200:
    # HTML 파싱
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    print(soup)
    
    # 웹 페이지의 제목 가져오기
    # con = soup.select_one('#nav-review > div:nth-child(5) > div.list--wrap--yFAThmi > div > div:nth-child(1) > div > div.list--itemContent--onkwE7H > div:nth-child(1) > div.list--itemReview--xQUhO78')
    con = soup.find('div', class_='list--itemReview--xQUhO78')
    print(f'웹 페이지 일부 크롤링 : {con}')
else:
    print(f'웹 페이지 요청 실패: {response.status_code}')

# 이해를 위한 간단한 크롤링 예시
# BeautifulSoup 이거 안쓸거임
