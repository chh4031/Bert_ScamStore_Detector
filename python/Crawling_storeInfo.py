from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


class SafeChrome(uc.Chrome):
    def __del__(self):
        pass  # 자동 소멸 시 quit() 호출 방지

def ShoreInfo(URL):
    driver = None

    Product_name_data = ""
    Store_open_data = ""
    Store_name_data = ""
    Store_delivery_data = ""
    Store_locate_data = ""

    try:
        start_time = time.time()

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

        time.sleep(4)
        driver.refresh()
        time.sleep(4)

        # 마우스 커서 먼저 올려두는 부분이 필요함(커서가 올라가야 작동함 ㅇㅇ)
        # 마우스를 올릴 요소 찾기
        try:
            time.sleep(1)
            hover_element = driver.find_element(By.CLASS_NAME, 'store-detail--wrap--IhR4e1j')
            time.sleep(1)
        # 마우스 커서를 요소 위로 이동
            actions_hover = ActionChains(driver)
            time.sleep(1)
            actions_hover.move_to_element(hover_element).perform()
            time.sleep(1)
        except Exception as e:
            print(f"마우스 이동 실패 {e}")

        time.sleep(1)

        try:
            # 상품 이름 가져오는거 이거 중요한게 "2025", "새로운" 키워드가 있으면 사기 확률이 높아진다고 함.
            Product_name = driver.find_element(By.CLASS_NAME, "title--wrap--UUHae_g")
            Product_name_h1 = Product_name.find_element(By.TAG_NAME, 'h1')
            Product_name_data = Product_name_h1.text
            print(f"상품명 가져오기 : {Product_name_data}")

            Store_open = driver.find_element(By.XPATH, '//td[contains(text(), "영업개시일")]/following-sibling::td')
            Store_open_data = Store_open.text
            print(f"영업개시일 가져오기 : {Store_open_data}")

            Store_name = driver.find_element(By.XPATH, '//td[contains(text(), "스토어명")]/following-sibling::td')
            Store_name_data = Store_name.text
            print(f"스토어명 가져오기 : {Store_name_data}")

            Store_locate = driver.find_element(By.XPATH, '//td[contains(text(), "영업소재지")]/following-sibling::td')
            Store_locate_data = Store_locate.text
            print(f"영업소재지 가져오기 : {Store_locate_data}")


            driver.execute_script("document.elementFromPoint(0, 0).click();")
            time.sleep(2)

            click_element = driver.find_element(By.CLASS_NAME, 'shipping--content--ulA3urO')
            actions_click = ActionChains(driver)
            actions_click.click(click_element).perform()

            time.sleep(2)

            try:
                Store_delivery = driver.find_element(By.CLASS_NAME, 'dynamic-shipping')
                Store_delivery_child = Store_delivery.find_element(By.CSS_SELECTOR,'span:nth-child(4) span')
                Store_delivery_data = Store_delivery_child.text
            except:
                Store_delivery_data = "출발지 China"
                pass
            print(f"배송정보 가져오기 : {Store_delivery_data}")

        except Exception as e:
            print(f"데이터 가져오기 실패 : {e}")

    finally:
        # 웹 드라이버 종료
        if driver:
            driver.quit()

    parsed_date = datetime.strptime(Store_open_data, "%m월 %d, %Y")
    formatted_date = parsed_date.strftime("%Y-%m-%d")

    storeTotal = {
        'ProductName' : Product_name_data,
        'StoreOpen' : formatted_date,
        'StoreName' : Store_name_data,
        'StoreDeli' : Store_delivery_data,
        'StoreCountry' : Store_locate_data
    }

    # 현재 진행중인 크롤링 코드

    end_time = time.time()
    check_time = end_time - start_time
    print(f"실행시간 : {check_time: .2f} 초")

    return  storeTotal

# 테스트 코드
# ShoreInfo()