from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time

class SafeChrome(uc.Chrome):
    def __del__(self):
        pass  # 자동 소멸 시 quit() 호출 방지
        
def Choice(URL):
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

        url = URL
        driver.get(url)

        choice_Data = ""

        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        
        # 초이스 정보 가져오기
        try:
            choice_Info = driver.find_element(By.CLASS_NAME, "choice-mind--box--fJKH05M")
            choice_Info_element = choice_Info.find_element(By.TAG_NAME, 'span')
            choice_Info_text = choice_Info_element.text
            print(f"초이스 태그 정보 : {choice_Info_text}")
            choice_Data = choice_Info_text

        except Exception as e:
            print(f"choice 정보 가져오기 실패 : {e}")
            choice_Data = "정보없음"

    finally:
        # 웹 드라이버 종료
        if driver:
            driver.quit()

    # 현재 진행중인 크롤링 코드
    # 각 초이스 정보에 해당하는 부분
    # "약속", "AliExpress의 약속" => 초이스 상품, "서비스 약속" => 일반 상품

    end_time = time.time()
    check_time = end_time - start_time
    print(f"실행시간 : {check_time: .2f} 초")

    return choice_Data

# 테스트 실행용
# Choice()