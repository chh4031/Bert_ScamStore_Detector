from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
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
url = "https://ko.aliexpress.com/item/1005008743587979.html?spm=a2g0o.home.pcJustForYou.24.717b70f46q8HGw&gps-id=pcJustForYou&scm=1007.40170.414127.0&scm_id=1007.40170.414127.0&scm-url=1007.40170.414127.0&pvid=dbf82787-6d0c-4e22-8988-7af7a91cefbd&_t=gps-id:pcJustForYou,scm-url:1007.40170.414127.0,pvid:dbf82787-6d0c-4e22-8988-7af7a91cefbd,tpp_buckets:668%232846%238109%231935&pdp_ext_f=%7B%22order%22%3A%22359%22%2C%22eval%22%3A%221%22%2C%22sceneId%22%3A%223562%22%7D&pdp_npi=4%40dis%21USD%2116.40%2116.40%21%21%21119.89%21119.89%21%40212e508f17440945999805214e9dd1%2112000046485669946%21rec%21KR%212809048098%21X&utparam-url=scene%3ApcJustForYou%7Cquery_from%3A"
driver.get(url)

time.sleep(1)

# 초이스 정보 가져오기
try:
    choice_Info = driver.find_element(By.CLASS_NAME, "choice-mind--box--fJKH05M")
    choice_Info_element = choice_Info.find_element(By.TAG_NAME, 'span')
    choice_Info_text = choice_Info_element.text
    print(f"초이스 태그 정보 : {choice_Info_text}")

except Exception as e:
    print(f"정보 가져오기 실패 : {e}")

# 웹 드라이버 종료
driver.quit()

# 현재 진행중인 크롤링 코드
# 각 초이스 정보에 해당하는 부분
# "약속", "AliExpress의 약속" => 초이스 상품, "서비스 약속" => 일반 상품