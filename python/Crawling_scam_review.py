from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time

class SafeChrome(uc.Chrome):
    def __del__(self):
        pass  # 자동 소멸 시 quit() 호출 방지

def Review_Scam(URL):
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

        # 웹 사이트 가져오기
        url = URL
        driver.get(url)

        time.sleep(5)

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

        TT = round(scam_num/total_num*100, 2)

        print(f"총 가져온 1점리뷰갯수 : {total_num}") #TR
        print(f"총 가져온 사기리뷰갯수 : {scam_num}") #TS
        print(f"사기 리뷰 비율 : {TT}% <= (전체의 몇 %)") #TT

        total_info = {'TR' : total_num, 'TS' : scam_num, 'TT = %' : TT}

    finally:
    # 웹 드라이버 종료
        if driver:
            driver.quit()

    end_time = time.time()
    check_time = end_time - start_time
    print(f"실행시간 : {check_time: .2f} 초")
    # 그냥 리뷰데이터 가져오는 거에서 들고오는거라 쉽게 가능함
    # 사실상 코드 자체는 동일

    return total_info

# 테스트용 코드
# Review_Scam()