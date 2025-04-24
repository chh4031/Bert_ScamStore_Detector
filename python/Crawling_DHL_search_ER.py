from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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



# 웹 드라이버 설정 => 일단 설정해줘야함(만약 gpu 하드웨어 가속 오류 등등 나오면), 이전 설정

options.add_argument("--disable-gpu")  # GPU 하드웨어 가속 비활성화
options.add_argument("--no-sandbox")  # 샌드박스 비활성화

# 로봇피하는거라함
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

# 이 부분은 자동화 봇을 회피하는 부분(크롤링 시 문제는 로봇이 아닙니다와 같이 봇 감지를 하는 경우가 빈번함 => 다수 사용자 접속시 문제 발생)
options.add_argument("disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")


# 웹 드라이버 설정 => 기본설정, 만약 위에서 우회 피하기로 디버그 모드로 실행했다면 무조건 비활성화할것
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 웹 페이지 열기 => 크롤링 할 웹 페이지 지정(나중에 사용자가 넣는 페이지로 써야될듯)
url = "https://ko.aliexpress.com/item/1005008743333045.html?spm=a2g0o.productlist.main.1.4e0022aaxS5I8w&algo_pvid=ea948eee-f464-4482-a5fa-5e0cea3d64ee&algo_exp_id=ea948eee-f464-4482-a5fa-5e0cea3d64ee-0&pdp_ext_f=%7B%22order%22%3A%22-1%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%21732.52%21366.26%21%21%215354.66%212677.33%21%402140f54217440977325418021ed296%2112000046484163811%21sea%21KR%212809048098%21X&curPageLogUid=6l7C5JgLphfI&utparam-url=scene%3Asearch%7Cquery_from%3A"
driver.get(url)

time.sleep(1)

# 웹에서 전체 탐색을 우선적으로 해야해서 스크롤먼저 작성

# 페이지 스크롤을 전체 페이지로 해야 작동한다. html로 작동해야 된다. 아니면 작동하지 않는다
try:
    new_div = driver.find_element(By.TAG_NAME, 'html')

    print(new_div)

    scroll_times = 1
    scroll_pause_time = 2

    for _ in range(scroll_times):
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", new_div)
        print("스크롤완료")
        time.sleep(scroll_pause_time)

except Exception as e:
    print(f"스크롤실패 에러 : {e}")

time.sleep(1)

# 왜 본문 내용 못가져오는지는 의문 - 방법이 없음 가져올 수 없음. Xpath 등을 포함한 모든 방법을 사용하였으나 요소 자체를 못 가져옴
# try:
#     DHL_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='product-description']/div/div/div/div/div")))
#     print(DHL_search.text)

# except Exception as e:
#     print(f"감지 에러 : {e}")

# 웹 드라이버 종료
driver.quit()

# 현재 진행중인 크롤링 코드
# 로봇 우회하는 디버그 코드 있으니 꼭 참고
# 맛가서 안되니깐 그냥 스크롤 하는 부분만 볼것