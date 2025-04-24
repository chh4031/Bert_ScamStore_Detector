from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess

# Selenium 설정
options = Options()

# 크롬 디버깅 모드 실행 => 우회 피하기, 디버그 모드 실행임. 창이 2개 안뜨는지만 확인할것;; 신규설정
subprocess.Popen(r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"')

# Selenium 설정
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# ChromeDriver 자동 설치 및 Service 객체 사용
chromedriver_autoinstaller.install()
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
service = Service(f'./{chrome_ver}/chromedriver.exe')

try:
    driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
    print(f"오류 발생: {e}")
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(service=service, options=options)

driver.implicitly_wait(10)

# 웹 드라이버 설정 => 일단 설정해줘야함(만약 gpu 하드웨어 가속 오류 등등 나오면)
options.add_argument("--disable-gpu")  # GPU 하드웨어 가속 비활성화
options.add_argument("--no-sandbox")  # 샌드박스 비활성화

# 이 부분은 자동화 봇을 회피하는 부분(크롤링 시 문제는 로봇이 아닙니다와 같이 봇 감지를 하는 경우가 빈번함 => 다수 사용자 접속시 문제 발생)
options.add_argument("disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

# 웹 사이트 가져오기
url = "https://ko.aliexpress.com/item/1005007802833987.html?spm=a2g0o.detail.pcDetailTopMoreOtherSeller.3.7d95KakZKakZOD&gps-id=pcDetailTopMoreOtherSeller&scm=1007.14452.398466.0&scm_id=1007.14452.398466.0&scm-url=1007.14452.398466.0&pvid=8885d4f5-305f-484a-99a5-805421dd38c8&_t=gps-id:pcDetailTopMoreOtherSeller,scm-url:1007.14452.398466.0,pvid:8885d4f5-305f-484a-99a5-805421dd38c8,tpp_buckets:668%232846%238109%231935&pdp_ext_f=%7B%22order%22%3A%22738%22%2C%22eval%22%3A%221%22%2C%22sceneId%22%3A%2230050%22%7D&pdp_npi=4%40dis%21USD%2114.47%2113.64%21%21%21106.17%21100.10%21%40212e509017441754386225004e3218%2112000042254255576%21rec%21KR%212809048098%21X&utparam-url=scene%3ApcDetailTopMoreOtherSeller%7Cquery_from%3A&search_p4p_id=202504082210386693143721156405675734_2"
driver.get(url)

time.sleep(1)

# 더보기 버튼 클릭으로 리뷰 데이터 가져오기(이거는 한번만 누를수 있게 구성)
try:
    more_button = driver.find_element(By.CSS_SELECTOR, ".comet-v2-btn.comet-v2-btn-slim.comet-v2-btn-large.comet-v2-btn-important")
    # print(more_button)
    driver.execute_script("arguments[0].click();", more_button)
    time.sleep(5)
except Exception as e:
    print(f"버튼 누르기 실패: {e}")

try:
    m_button = driver.find_elements(By.CSS_SELECTOR, ".filter--filterItem--udTNLrr")
    # print(m_button)
    driver.execute_script("arguments[0].click();", m_button[17])
    # 여기서 가져와야 하는 버튼은 17번째임. 별 1개 짜리 리뷰를 가져올 거기 때문
    print("버튼 눌러짐")
    time.sleep(5)
except Exception as e:
    print(f"버튼 안눌러짐 : {e}")

time.sleep(5)

try:
    new_div = driver.find_element(By.CSS_SELECTOR, ".comet-v2-modal-body")  # 새로운 div 요소의 CSS 셀렉터를 사용(이거 이상하게 body쪽을 잡아야함)

    # 스크롤 횟수 설정 => 이방법은 일부만 가져오는 방식(다 가져오면 시간 오지게 걸림)
    scroll_times = 3  # 스크롤을 3번만 내림
    scroll_pause_time = 2  # 스크롤 후 대기 시간 (초) => 스크롤 후 대기없이 하면 오류터짐 => 특히 데이터를 모두 로드 못하는게 이유

    for _ in range(scroll_times): #빈벅 횟수만 중요해서 변수지정 안할때 _ 사용
        # 새로운 div 요소 내에서 스크롤을 아래로 내림(이게 매크로처럼 딱딱 처리하는 방식)
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", new_div)
        time.sleep(scroll_pause_time)  # 페이지가 로드될 시간(위와 같은 이유)

 # 리뷰 데이터를 리스트에 저장 => 전처리 버전, 일단 리스트에만 저장, strip()에 인자 암거도 안넣으면 공백을 제거하는거임
    reviews = driver.find_elements(By.CSS_SELECTOR, ".list--itemReview--xQUhO78")
    review_list = [review.text for review in reviews if review.text.strip()]

except Exception as e:
    print(f"존재하지 않는 리뷰 : {e}")
    review_list = []

total_num = 0
scam_num = 0

# 사기나 가짜 같은 키워드 있는거만 가져오면 될듯
for review in review_list:
    total_num += 1
    if "사기" in review or "가짜" in review or "스캠" in review:
        scam_num += 1
        print(review)

print(f"총 가져온 1점리뷰갯수 : {total_num}")
print(f"총 가져온 사기리뷰갯수 : {scam_num}")
print(f"사기 리뷰 비율 : {round(scam_num/total_num*100, 2)}% <= (전체의 몇 %)")

driver.quit()
# 그냥 리뷰데이터 가져오는 거에서 들고오는거라 쉽게 가능함
# 사실상 코드 자체는 동일