# 일단 selenium이 크롤링함
# webdriver로 크롬에서 하는 방식 => 젤 성능이 나은듯?
# BeautifulSoup는 안씀 => 동적 웹은 처리못함 특히 자바스크립트 같은거

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

# 웹 드라이버 설정 => 기본설정
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 웹 페이지 열기 => 크롤링 할 웹 페이지 지정(나중에 사용자가 넣는 페이지로 써야될듯)
# url = "https://ko.aliexpress.com/item/1005008763672419.html?spm=a2g0o.home.pcJustForYou.3.707f70f4wWLHcK&gps-id=pcJustForYou&scm=1007.13562.416251.0&scm_id=1007.13562.416251.0&scm-url=1007.13562.416251.0&pvid=905ee17a-e3cf-4bab-887e-5c332df5ed6e&_t=gps-id:pcJustForYou,scm-url:1007.13562.416251.0,pvid:905ee17a-e3cf-4bab-887e-5c332df5ed6e,tpp_buckets:668%232846%238116%232002&pdp_ext_f=%7B%22order%22%3A%221%22%2C%22eval%22%3A%221%22%2C%22sceneId%22%3A%223562%22%7D&pdp_npi=4%40dis%21USD%2188.06%2144.03%21%21%21643.73%21321.86%21%402102f0c917440933319353331eea0e%2112000046566095170%21rec%21KR%212809048098%21X&utparam-url=scene%3ApcJustForYou%7Cquery_from%3A#nav-review"
url = "https://ko.aliexpress.com/item/1005006802925639.html?spm=a2g0o.order_list.order_list_main.15.d975140fLaQd7d&gatewayAdapt=glo2kor"
driver.get(url)

time.sleep(1)

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
    # print(more_button)
    driver.execute_script("arguments[0].click();", more_button)
    time.sleep(5)  # 페이지가 로드 시간(이거 안주면 페이지 로드 안되는 경우 생김)
except Exception as e:
    print(f"버튼 누르기 실패: {e}")

try:
    m_button = driver.find_elements(By.CSS_SELECTOR, ".filter--filterItem--udTNLrr")
    # print(m_button)
    driver.execute_script("arguments[0].click();", m_button[12])
    # 하 이거 m_button으로 불러와지는 요소가 여러개임 elements를 써서 그럼. 이때 해당 웹 페이지에서는 뒤에 깔려있는 거도 있기 때문에 총 18개임 단 0~8까지 같고, 9~17까지 같음. 그래서 12번째 요소를 가져오면 됨
    print("버튼 눌러짐")
    time.sleep(5)
except Exception as e:
    print(f"버튼 안눌러짐 : {e}")

# 새로운 div 요소가 뜰때까지 대기(이게 새로운 페이지<더보기>를 띄우는데 먼저 안뜨면 오류발생함)
time.sleep(5)  # 페이지가 로드될 시간(위와 같은 이유로 사용함)

# 새로운 div 요소 찾기(이게 <더보기> 버튼 누를때 나오는 div임, 이거 더보기 안누르면 안날라오니깐 예외처리해야함. 또한 다른 더보기 눌러도 안날라와서 예외처리해야함)
try:
    new_div = driver.find_element(By.CSS_SELECTOR, ".comet-v2-modal-body")  # 새로운 div 요소의 CSS 셀렉터를 사용(이거 이상하게 body쪽을 잡아야함)

    # 스크롤 횟수 설정 => 이방법은 일부만 가져오는 방식(다 가져오면 시간 오지게 걸림)
    scroll_times = 3  # 스크롤을 3번만 내림
    scroll_pause_time = 2  # 스크롤 후 대기 시간 (초) => 스크롤 후 대기없이 하면 오류터짐 => 특히 데이터를 모두 로드 못하는게 이유

    for _ in range(scroll_times): #빈벅 횟수만 중요해서 변수지정 안할때 _ 사용
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

    # # 리뷰 데이터 가져오기 => 근데 이게 공백 데이터도 가져오는 문제가 있음 => 나중에 전처리로 해결 가능(예를 들어 별점만 주고 리뷰는 안쓴이런것들)
    # reviews = driver.find_elements(By.CSS_SELECTOR, ".list--itemReview--xQUhO78")
    # for review in reviews:
    #     print(review.text)

    # 리뷰 데이터를 리스트에 저장 => 전처리 버전, 일단 리스트에만 저장, strip()에 인자 암거도 안넣으면 공백을 제거하는거임
    reviews = driver.find_elements(By.CSS_SELECTOR, ".list--itemReview--xQUhO78")
    review_list = [review.text for review in reviews if review.text.strip()]

except Exception as e:
    print(f"존재하지 않는 리뷰 : {e}")
    review_list = []

# print(review_list)
# 이게 리스트로 그냥 전부 가져와보는거

# 리뷰 리스트 출력 => 전처리 된거만 출력
for review in review_list:
    print(review)

# 웹 드라이버 종료
driver.quit()

# 현재 진행중인 크롤링 코드