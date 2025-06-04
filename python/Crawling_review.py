# 일단 selenium이 크롤링함
# webdriver로 크롬에서 하는 방식 => 젤 성능이 나은듯?
# BeautifulSoup는 안씀 => 동적 웹은 처리못함 특히 자바스크립트 같은거

from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SafeChrome(uc.Chrome):
    def __del__(self):
        pass  # 자동 소멸 시 quit() 호출 방지

def Review_Crawing(URL):
    driver = None

    try:
        start_time = time.time()

        options = uc.ChromeOptions()

        # 웹 드라이버 설정 => 일단 설정해줘야함(만약 gpu 하드웨어 가속 오류 등등 나오면)
        options.add_argument("--disable-gpu")  # GPU 하드웨어 가속 비활성화
        options.add_argument("--no-sandbox")  # 샌드박스 비활성화
        options.add_argument("--disable-dev-shm-usage")

        # 이 부분은 자동화 봇을 회피하는 부분(크롤링 시 문제는 로봇이 아닙니다와 같이 봇 감지를 하는 경우가 빈번함 => 다수 사용자 접속시 문제 발생)
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

        # 웹 페이지 열기 => 크롤링 할 웹 페이지 지정(나중에 사용자가 넣는 페이지로 써야될듯)
        
        driver = SafeChrome(options=options)
        driver.implicitly_wait(10)
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # 웹 페이지 열기 => 크롤링 할 웹 페이지 지정(나중에 사용자가 넣는 페이지로 써야될듯)
        url = URL
        driver.get(url)

        time.sleep(4)
        # driver.refresh()
        # time.sleep(4)
        
        # wait = WebDriverWait(driver, 15)

        # 더보기 버튼 클릭으로 리뷰 데이터 가져오기(이거는 한번만 누를수 있게 구성)
        try:
            # Xpath로 확실하게 선택하기 => 이거 상품 페이지마다 태그명이 좀 다름
            more_button = driver.find_element(By.XPATH, '//div[contains(text(), "지역 검토")]')
            # print(more_button)
            driver.execute_script("arguments[0].click();", more_button)
            time.sleep(3)  # 페이지가 로드 시간(이거 안주면 페이지 로드 안되는 경우 생김)
        except Exception as e:
            print(f"버튼 누르기 실패: {e}")

            time.sleep(1)

        try:
            # m_button = driver.find_elements(By.CSS_SELECTOR, ".filter--filterItem--udTNLrr")
            m_button = driver.find_elements(By.XPATH, '//div[contains(text(), "지역 검토")]')
            # print(m_button)
            # driver.execute_script("arguments[0].click();", m_button[12])
            driver.execute_script("arguments[0].click();", m_button[1])
            # 테스트케이스 2 : 17, 테스트케이스 3 : 12
            # 하 이거 m_button으로 불러와지는 요소가 여러개임 elements를 써서 그럼. 이때 해당 웹 페이지에서는 뒤에 깔려있는 거도 있기 때문에 총 18개임 단 0~8까지 같고, 9~17까지 같음. 그래서 12번째 요소를 가져오면 됨
            print("버튼 눌러짐")
            time.sleep(2)
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

            # 리뷰 데이터를 리스트에 저장 => 전처리 버전, 일단 리스트에만 저장, strip()에 인자 암거도 안넣으면 공백을 제거하는거임
            reviews = driver.find_elements(By.CSS_SELECTOR, ".list--itemReview--xQUhO78")
            review_list = [review.text for review in reviews if review.text.strip()]

        except Exception as e:
            print(f"존재하지 않는 리뷰 : {e}")
            review_list = []

        # 리뷰 리스트 출력 => 전처리 된거만 출력
        # for review in review_list:
        #     print(review)
        # print(len(review_list))

    finally:
        # 웹 드라이버 종료
        if driver:
            driver.quit()

    end_time = time.time()
    check_time = end_time - start_time
    print(f"실행시간 : {check_time: .2f} 초")

    return review_list

# 테스트용 코드
# Review_Crawing()