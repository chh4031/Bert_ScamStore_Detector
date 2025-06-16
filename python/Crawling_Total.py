from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import undetected_chromedriver as uc
import time


class SafeChrome(uc.Chrome):
    def __del__(self):
        pass  # 자동 소멸 시 quit() 호출 방지


def init_driver():
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.68 Safari/537.36")

    driver = SafeChrome(options=options)
    driver.implicitly_wait(10)
    return driver


def get_choice_info(driver):
    choice_Data = ""
    try:
        time.sleep(2)
        # driver.refresh()
        # time.sleep(2)

        choice_Info = driver.find_element(By.CLASS_NAME, "choice-mind--box--fJKH05M")
        choice_Info_element = choice_Info.find_element(By.TAG_NAME, 'span')
        choice_Data = choice_Info_element.text
        print(f"초이스 태그 정보 : {choice_Data}")
    except Exception as e:
        print(f"choice 정보 가져오기 실패 : {e}")
        choice_Data = "정보없음"

    return choice_Data


def get_reviews(driver):
    review_list = []
    try:
        time.sleep(4)
        try:
            more_button = driver.find_element(By.XPATH, '//button[.//span[text()="더 보기"]]')
            driver.execute_script("arguments[0].click();", more_button)
            time.sleep(3)
        except Exception as e:
            print(f"버튼 누르기 실패: {e}")
            time.sleep(1)

        try:
            m_button = driver.find_elements(By.XPATH, '//div[contains(text(), "지역 검토")]')
            driver.execute_script("arguments[0].click();", m_button[1])
            print("버튼 눌러짐")
            time.sleep(2)
        except Exception as e:
            print(f"버튼 안눌러짐 : {e}")

        time.sleep(3)

        new_div = driver.find_elements(By.CSS_SELECTOR, ".comet-v2-modal-body")

        scroll_times = 3
        scroll_pause_time = 2 

        for _ in range(scroll_times):
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", new_div[1])
            time.sleep(scroll_pause_time)

        reviews = driver.find_elements(By.CSS_SELECTOR, ".list--itemReview--xQUhO78")
        review_list = [review.text for review in reviews if review.text.strip()]
    except Exception as e:
        print(f"존재하지 않는 리뷰 : {e}")

    return review_list


def get_store_info(driver):
    Product_name_data = ""
    Store_open_data = ""
    Store_name_data = ""
    Store_delivery_data = ""
    Store_locate_data = ""

    try:
        time.sleep(4)
        # driver.refresh()
        # time.sleep(4)

        try:
            time.sleep(1)
            hover_element = driver.find_element(By.CLASS_NAME, 'store-detail--wrap--IhR4e1j')
            time.sleep(1)
            actions_hover = ActionChains(driver)
            time.sleep(1)
            actions_hover.move_to_element(hover_element).perform()
            time.sleep(1)
        except Exception as e:
            print(f"마우스 이동 실패 {e}")
        time.sleep(1)

        try:
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
                Store_delivery_child = Store_delivery.find_element(By.CSS_SELECTOR, 'span:nth-child(4) span')
                Store_delivery_data = Store_delivery_child.text
            except:
                Store_delivery_data = "출발지 China"
            print(f"배송정보 가져오기 : {Store_delivery_data}")
        except Exception as e:
            print(f"데이터 가져오기 실패 : {e}")
    except:
        pass

    try:
        Close = driver.find_elements(By.CLASS_NAME, 'comet-v2-modal-close')
        Close_click = ActionChains(driver)
        Close_click.click(Close[0]).perform()    
    except Exception as e:
        print(f"안꺼짐", e)

    try:
        parsed_date = datetime.strptime(Store_open_data, "%m월 %d, %Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
    except:
        formatted_date = "0000-00-00"

    storeTotal = {
        'ProductName': Product_name_data,
        'StoreOpen': formatted_date,
        'StoreName': Store_name_data,
        'StoreDeli': Store_delivery_data,
        'StoreCountry': Store_locate_data
    }

    return storeTotal


def crawl_all(url):
    driver = init_driver()
    choice_Data = ""
    review_list = []
    storeTotal = {}

    try:
        start_time = time.time()

        driver.get(url)

        choice_Data = get_choice_info(driver)
        storeTotal = get_store_info(driver)
        review_list = get_reviews(driver)

        end_time = time.time()
        print(f"총 실행 시간: {end_time - start_time:.2f}초")

    finally:
        driver.quit()

    return choice_Data, review_list, storeTotal
    