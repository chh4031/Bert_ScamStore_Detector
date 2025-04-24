from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess

import re

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

# 웹 페이지 열기 => 크롤링 할 웹 페이지 지정(나중에 사용자가 넣는 페이지로 써야될듯)
# url = "https://ko.aliexpress.com/item/1005007802833987.html?spm=a2g0o.detail.pcDetailTopMoreOtherSeller.3.7d95KakZKakZOD&gps-id=pcDetailTopMoreOtherSeller&scm=1007.14452.398466.0&scm_id=1007.14452.398466.0&scm-url=1007.14452.398466.0&pvid=8885d4f5-305f-484a-99a5-805421dd38c8&_t=gps-id:pcDetailTopMoreOtherSeller,scm-url:1007.14452.398466.0,pvid:8885d4f5-305f-484a-99a5-805421dd38c8,tpp_buckets:668%232846%238109%231935&pdp_ext_f=%7B%22order%22%3A%22738%22%2C%22eval%22%3A%221%22%2C%22sceneId%22%3A%2230050%22%7D&pdp_npi=4%40dis%21USD%2114.47%2113.64%21%21%21106.17%21100.10%21%40212e509017441754386225004e3218%2112000042254255576%21rec%21KR%212809048098%21X&utparam-url=scene%3ApcDetailTopMoreOtherSeller%7Cquery_from%3A&search_p4p_id=202504082210386693143721156405675734_2"
# url = "https://ko.aliexpress.com/item/1005008743738417.html?spm=a2g0o.home.pcJustForYou.9.1f7b70f4gZ2wly&gps-id=pcJustForYou&scm=1007.40170.414127.0&scm_id=1007.40170.414127.0&scm-url=1007.40170.414127.0&pvid=a66d2ee1-8c19-4321-8ae3-56ac30b5e96b&_t=gps-id:pcJustForYou,scm-url:1007.40170.414127.0,pvid:a66d2ee1-8c19-4321-8ae3-56ac30b5e96b,tpp_buckets:668%232846%238109%231935&pdp_ext_f=%7B%22order%22%3A%229%22%2C%22eval%22%3A%221%22%2C%22sceneId%22%3A%223562%22%7D&pdp_npi=4%40dis%21USD%2135.00%2117.50%21%21%21256.79%21128.39%21%40210123bc17441747466616538e5ca9%2112000046485625949%21rec%21KR%212809048098%21XZ&utparam-url=scene%3ApcJustForYou%7Cquery_from%3A"
# url = "https://ko.aliexpress.com/item/1005008749980490.html?spm=a2g0o.productlist.main.17.6d661kvc1kvc12&algo_pvid=406be03c-1525-47dc-bbf5-8b1b2d67c298&algo_exp_id=406be03c-1525-47dc-bbf5-8b1b2d67c298-16&pdp_ext_f=%7B%22order%22%3A%22-1%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%2112.49%219.99%21%21%2112.49%219.99%21%40212e509017445634775886600e6450%2112000046658674118%21sea%21KR%212809048098%21X&curPageLogUid=rgNDickVq7di&utparam-url=scene%3Asearch%7Cquery_from%3A"
url = "https://ko.aliexpress.com/item/1005008781508727.html?spm=a2g0o.productlist.main.15.6d661kvc1kvc12&algo_pvid=406be03c-1525-47dc-bbf5-8b1b2d67c298&algo_exp_id=406be03c-1525-47dc-bbf5-8b1b2d67c298-14&pdp_ext_f=%7B%22order%22%3A%221%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%2140.41%2120.20%21%21%21294.34%21147.17%21%40212e509017445634775886600e6450%2112000046643902417%21sea%21KR%212809048098%21X&curPageLogUid=4ezGOOSIzkXF&utparam-url=scene%3Asearch%7Cquery_from%3A"
driver.get(url)

time.sleep(1)

# reviewer--wrap--vGS7G6P로 가져올 수 있는 평점, 리뷰, 판매 댓수 가져오기 (판매자 제외) => 이쪽 판매자쪽
# 정규 표현식 사용됨, 일부는 나중에 가중치 작업을 위해 좀 잘라냄

try:
    # 이거 일단 평점 가져오는거
    store_score = 0
    try:
        total_info = driver.find_element(By.CLASS_NAME, "reviewer--wrap--vGS7G6P")
        total_score = total_info.find_element(By.TAG_NAME, 'strong')
        print(total_score.text)
        total_score_text = float(total_score.text)

        try:
            total_review = total_info.find_element(By.CLASS_NAME, 'reviewer--reviews--cx7Zs_V')
            total_review_text = re.findall(r'\d+', total_review.text)[0]
        except:
            store_sell = driver.find_element(By.XPATH, "//span[contains(text(), '누적판매')]")
            store_sell_text = re.findall(r'\d+,\d+\+', store_sell.text)[0]
            store_sell_text_number = re.findall(r'\d+,\d+', store_sell.text)[0]
            store_score = total_score_text
            total_score_text = 0
            total_review_text = 0

    except Exception as e:
        total_score_text = 0
        total_review_text = 0
        store_score = 0
        store_sell_text = 0
        store_sell_text_number = 0

    try:
        total_sell = total_info.find_element(By.CLASS_NAME, "reviewer--sold--ytPeoEy")
        total_sell_text = re.findall(r'\d+\+', total_sell.text)
        # print(total_sell_text)
        # 리스트가 비어있는지 확인, 비어있지 않으면 true임, 이게 그냥 판매갯수만 있는 경우임
        total_sell_text_number = re.findall(r'\d+', total_sell.text)[0]
        if total_sell_text:
            pass
        else:
            total_sell_text.append(total_sell_text_number)
    except:
        total_sell_text = 0
        total_sell_text_number = 0
        pass
    
except Exception as e:
    print(f"정보 가져오기 실패 : {e}")

print(f"제품 평점 : {total_score_text}")
print(f"제품 리뷰 갯수 : {total_review_text}")
print(f"제품 판매 갯수 : {total_sell_text}, 전처리 판매 갯수 데이터 : {total_sell_text_number}")
print(f"스토어 평점 : {store_score}")
print(f"스토어 누적 판매 갯수 : {store_sell_text}, 전처리 판매 갯수 데이터 : {store_sell_text_number}")

# 상점명이 나오는 부분에서 가져오는 평점 => 이거 짜놔야함.

driver.quit()

"""
이슈사항으로 각 페이지마다 다른 전체 리뷰, 평점, 판매 갯수가 다르게 표기된 경우가 있음.
html에서 해당 부분은 reviewer--wrap--vGS7G6P로 동일하긴함.
이 안에서 가져오는 항목들이 달라질수 있다는것.
분기처리의 기준도 애매함. 되는게 있고 안되는게 있고함.

단. 아래 클래스는 해당 페이지에서 없는 경우에는 그냥 오류 뱉고 끝나긴함.
없는 경우도 존재함.
해당 제품 리뷰 평점의 클래스 : reviewer--wrap--vGS7G6P => 안에서 strong으로 접근함.
    단 위의 경우가 없는 경우는 판매자 평점으로 넘아감 ㅇㅇ => 근데 클래스 자체는 동일한듯
    판매자 평점 리뷰의 경우는 일단 클래스에서 접근해서 XPath로 가져와야할듯 => 특정 텍스트 감지, 평점은 strong으로 기존으로 가능
해당 제품 판매 갯수의 클래스 : reviewer--sold--ytPeoEy => 전부 동일
해당 제품 리뷰 갯수의 클래스 : reviewer--reviews--cx7Zs_V => 전부 동일

걍 해당 제품에 대한 판매댓수만 가져올 수 있도록 구성, 전체 누적판매댓수는 그닥 필요없는 데이터일듯 => 걍 로직이 너무 복잡해짐 속도만 느려짐...

경우는 총 4개임
별점 + 평점 + 리뷰갯수 + 판매갯수(제품판매수)로 되어져 있는것 => 가능
https://ko.aliexpress.com/item/1005007802833987.html?spm=a2g0o.detail.pcDetailTopMoreOtherSeller.3.7d95KakZKakZOD&gps-id=pcDetailTopMoreOtherSeller&scm=1007.14452.398466.0&scm_id=1007.14452.398466.0&scm-url=1007.14452.398466.0&pvid=8885d4f5-305f-484a-99a5-805421dd38c8&_t=gps-id:pcDetailTopMoreOtherSeller,scm-url:1007.14452.398466.0,pvid:8885d4f5-305f-484a-99a5-805421dd38c8,tpp_buckets:668%232846%238109%231935&pdp_ext_f=%7B%22order%22%3A%22738%22%2C%22eval%22%3A%221%22%2C%22sceneId%22%3A%2230050%22%7D&pdp_npi=4%40dis%21USD%2114.47%2113.64%21%21%21106.17%21100.10%21%40212e509017441754386225004e3218%2112000042254255576%21rec%21KR%212809048098%21X&utparam-url=scene%3ApcDetailTopMoreOtherSeller%7Cquery_from%3A&search_p4p_id=202504082210386693143721156405675734_2
판매갯수(제품판매수)만 있는것 => 가능
https://ko.aliexpress.com/item/1005008743738417.html?spm=a2g0o.home.pcJustForYou.9.1f7b70f4gZ2wly&gps-id=pcJustForYou&scm=1007.40170.414127.0&scm_id=1007.40170.414127.0&scm-url=1007.40170.414127.0&pvid=a66d2ee1-8c19-4321-8ae3-56ac30b5e96b&_t=gps-id:pcJustForYou,scm-url:1007.40170.414127.0,pvid:a66d2ee1-8c19-4321-8ae3-56ac30b5e96b,tpp_buckets:668%232846%238109%231935&pdp_ext_f=%7B%22order%22%3A%229%22%2C%22eval%22%3A%221%22%2C%22sceneId%22%3A%223562%22%7D&pdp_npi=4%40dis%21USD%2135.00%2117.50%21%21%21256.79%21128.39%21%40210123bc17441747466616538e5ca9%2112000046485625949%21rec%21KR%212809048098%21XZ&utparam-url=scene%3ApcJustForYou%7Cquery_from%3A

판매갯수 + 스토어이름 + 평점 + 누적판매댓수(스토어 전체 판매수)로 되어져 있는것(동적텍스트형식) => 스토어 정보를 못 가져옴 => 뭘 해도 못가져옴 => 그냥 제품 얼마나 팔렸는가만 가져옴 그래서 위의 판매갯수만 있는 것과 데이터를 동일하게 가져옴. 단 둘의 차이는 초이스 차이임
https://ko.aliexpress.com/item/1005008781508727.html?spm=a2g0o.productlist.main.15.6d661kvc1kvc12&algo_pvid=406be03c-1525-47dc-bbf5-8b1b2d67c298&algo_exp_id=406be03c-1525-47dc-bbf5-8b1b2d67c298-14&pdp_ext_f=%7B%22order%22%3A%221%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%2140.41%2120.20%21%21%21294.34%21147.17%21%40212e509017445634775886600e6450%2112000046643902417%21sea%21KR%212809048098%21X&curPageLogUid=4ezGOOSIzkXF&utparam-url=scene%3Asearch%7Cquery_from%3A
스토어이름 + 평점 + 누적판매댓수(스토어 전체 판매수)로 되어져 있는것 => 가능
https://ko.aliexpress.com/item/1005008749980490.html?spm=a2g0o.productlist.main.17.6d661kvc1kvc12&algo_pvid=406be03c-1525-47dc-bbf5-8b1b2d67c298&algo_exp_id=406be03c-1525-47dc-bbf5-8b1b2d67c298-16&pdp_ext_f=%7B%22order%22%3A%22-1%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%2112.49%219.99%21%21%2112.49%219.99%21%40212e509017445634775886600e6450%2112000046658674118%21sea%21KR%212809048098%21X&curPageLogUid=rgNDickVq7di&utparam-url=scene%3Asearch%7Cquery_from%3A
"""