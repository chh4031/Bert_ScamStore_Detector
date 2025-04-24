"""
일단 selenium이 크롤링함
webdriver로 크롬에서 하는 방식 => 젤 성능이 나은듯?
BeautifulSoup는 안씀 => 동적 웹은 처리못함 특히 자바스크립트 같은거
일단 크롤링 해서 리뷰들 가져오는거 까진 가능함. 
이후 다른 거 크롤링할때 클래스 태그 따오는거 알아놔야함
밑에 코드에 있으니깐 다른꺼 따올때도 그렇게 사용하면 됨.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 웹 드라이버 설정 => 일단 설정해줘야함(만약 gpu 하드웨어 가속 오류 등등 나오면)
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")  # GPU 하드웨어 가속 비활성화
options.add_argument("--no-sandbox")  # 샌드박스 비활성화

# 웹 드라이버 설정 => 기본설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 웹 페이지 열기 => 크롤링 할 웹 페이지 지정(나중에 사용자가 넣는 페이지로 써야될듯)
url = "https://ko.aliexpress.com/item/1005006404381520.html?spm=a2g0o.order_list.order_list_main.4.d975140ftRvLSF&gatewayAdapt=glo2kor#nav-store"
driver.get(url)

# "더보기" 버튼 클릭 이 코드는 이상함 버튼만 누름;; 한번만 누르면 되므로 while 루트 필요없음 => 시험용 코드
# while True:
#     try:
#         # more_button = driver.find_element(By.CSS_SELECTOR, "#nav-review > div:nth-child(5) > button")
#         more_button = driver.find_element(By.CSS_SELECTOR, ".comet-v2-btn.comet-v2-btn-slim.comet-v2-btn-large.comet-v2-btn-important")
#         driver.execute_script("arguments[0].click();", more_button)
#         # more_button.click()
#         time.sleep(2)  # 페이지가 로드될 시간
#         print("버튼누르기 성공")
#     except:
#         print("버튼누르기 실패")
#         break  # 더보기 없으면 종료


# 더보기 버튼 클릭으로 리뷰 데이터 가져오기(이거는 한번만 누를수 있게 구성)
try:
    more_button = driver.find_element(By.CSS_SELECTOR, ".comet-v2-btn.comet-v2-btn-slim.comet-v2-btn-large.comet-v2-btn-important")
    driver.execute_script("arguments[0].click();", more_button)
    time.sleep(5)  # 페이지가 로드 시간(이거 안주면 페이지 로드 안되는 경우 생김)
except Exception as e:
    print(f"버튼 누르기 실패: {e}")

# 새로운 div 요소가 뜰때까지 대기(이게 새로운 페이지<더보기>를 띄우는데 먼저 안뜨면 오류발생함)
time.sleep(5)  # 페이지가 로드될 시간(위와 같은 이유로 사용함)

# 새로운 div 요소 찾기(이게 <더보기> 버튼 누를때 나오는 div임)
new_div = driver.find_element(By.CSS_SELECTOR, ".comet-v2-modal-body")  # 새로운 div 요소의 CSS 셀렉터를 사용(이거 이상하게 body쪽을 잡아야함)

# 스크롤 횟수 설정 => 이방법은 일부만 가져오는 방식(다 가져오면 시간 오지게 걸림)
scroll_times = 2  # 스크롤을 2번만 내림
scroll_pause_time = 2  # 스크롤 후 대기 시간 (초) => 스크롤 후 대기없이 하면 오류터짐 => 특히 데이터를 모두 로드 못하는게 이유

for _ in range(scroll_times):
    # 새로운 div 요소 내에서 스크롤을 아래로 내림(이게 매크로처럼 딱딱 처리하는 방식)
    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", new_div)
    time.sleep(scroll_pause_time)  # 페이지가 로드될 시간(위와 같은 이유)

# # 새로운 div 요소 내에서 스크롤 및 리뷰 데이터 가져오기 => 이방식은 전부 가져오는 방식
# last_height = driver.execute_script("return arguments[0].scrollHeight", new_div)
# while True:
#     # 새로운 div 요소 내에서 스크롤을 내림(이게 매크로처럼 딱딱 처리하는 방식, 근데 이거는 리뷰 마지막까지 내리기 때문에 진짜 오래 걸림)
#     driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", new_div)
#     time.sleep(5)  # 페이지가 로드될 시간(위와 같은 이유)
    
#     # 새로운 높이를 계산 => 이게 스크롤을 내리게 되면 아래 추가로 생겨서 높이를 새로 맞춰야하기 때문인듯?
#     new_height = driver.execute_script("return arguments[0].scrollHeight", new_div)
#     if new_height == last_height:
#         break
#     last_height = new_height

# 리뷰 데이터 가져오기 => 근데 이게 공백 데이터도 가져오는 문제가 있음 => 나중에 전처리로 해결 가능(예를 들어 별점만 주고 리뷰는 안쓴이런것들)
reviews = driver.find_elements(By.CSS_SELECTOR, ".list--itemReview--xQUhO78")
for review in reviews:
    print(review.text)

# 웹 드라이버 종료
driver.quit()