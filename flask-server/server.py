from flask import Flask, request, jsonify
from flask_cors import CORS

# python 폴더의 지정
import sys
sys.path.append("../python")

# 다른 폴더 python 코드 모듈 로드
import AI_Save_Model_use as AI
import Crawling_choiceInfo as CC
import Crawling_review as CR
import Crawling_scam_review as CSR
import Crawling_storeInfo as CS
import time
from datetime import datetime
import re

# import Test

# Test.Test()

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST'])

# api 통신으로 코드 가져옴

def handle_request():

    data = request.get_json()
    # url 데이터 저장
    url_data = data['message']
    print(data['message'])

    # 다른 파이썬 코드 실행될 부분들임.
    # 간단한 코드부터 시작할것!
    # 테스트용 url 붙여넣기로 쓸것

    # 초이스 여부
    received_Choice= CC.Choice(url_data)
    time.sleep(2)
    # 상점 정보
    received_StoreInfo = CS.ShoreInfo(url_data)
    time.sleep(2)
    # 스캠 리뷰 갯수, 비율 가져오기
    # received_ScamReview = CSR.Review_Scam(url_data)
    time.sleep(2)
    # 리뷰 정보 가져오기
    received_Review = CR.Review_Crawing(url_data)
    time.sleep(2)
    # 학습하기
    eval_Data = AI.Model(received_Review)
    # print(eval_Data)

    # 사기 위험도 결과 변수
    total = 0
    # 사기 위험도 계산 부분

    #  No promotion category label
    if received_Choice not in ["약속", "AliExpress의 약속", "  약속"]:
        total += 14
        Choice_select = "X"
        print("초이스 사기 검출")
    else:
        Choice_select = "O"

    #  Specific keywords exist in the product name
    if "새로운" in received_StoreInfo['ProductName'] or "2025" in received_StoreInfo['ProductName']:
        total += 7
        print("키워드 사기 검출")

    #  The store opening date is recent
    Format_StoreOpen = datetime.strptime(received_StoreInfo["StoreOpen"], "%Y-%m-%d")
    Standard_StoreOpen = datetime.strptime("2025-01-01", "%Y-%m-%d")

    if Format_StoreOpen > Standard_StoreOpen:
        total += 21
        print("오픈일 사기 검출")

    #  Not an official store
    if "Office" not in received_StoreInfo["StoreName"].lower():
        total += 25
        print("상점 이름 사기 검출")

    #  Shipping origin is Korea
    if "China" not in received_StoreInfo["StoreDeli"]:
        total += 4
        print("출발국 사기 검출")

    #  The store name is Number Shop
    if re.search(r'\d{8,}', received_StoreInfo["StoreName"]):
        total += 11
        print("숫자샵 사기 검출")

    #  Existence of manipulated reviews
    Fake_Review = eval_Data.count(1)
    Total_Review = len(eval_Data)
    total_Review_Num = round(Fake_Review/Total_Review * 100 * 0.18, 2)

    total += total_Review_Num

    print(f"최종 결과값 : {total}")

    # processed_data = {"message_html" : f"넘어간 데이터 : {received_Review}"}
    # processed_data = {"message_html": f"넘어간 데이터 : {received_Choice}\n{received_StoreInfo}\n{received_Review}\n{received_ScamReview}\n{eval_Data}"}
    processed_data = {
        "FK_result" : total,
        "FK_choice" : Choice_select,
        "FK_name" : received_StoreInfo["ProductName"],
        "FK_open" : Format_StoreOpen,
        "FK_country" : received_StoreInfo["StoreDeli"],
        "FK_fake" : Fake_Review,
        "FK_sname" : received_StoreInfo["StoreName"]
        }
    # print(processed_data)
    
    # 리액트에 결과 반환
    return jsonify(processed_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


# 사기 예시 1 https://ko.aliexpress.com/item/1005008625576340.html?pdp_npi
# 사기 예시 2 https://ko.aliexpress.com/item/1005008486195215.html?spm=a2g0o.store_pc_home.0.0.24d0433avJPLsh&gps-id=pcStoreLeaderboard&scm=1007.22922.271278.0&scm_id=1007.22922.271278.0&scm-url=1007.22922.271278.0&pvid=523291be-29ac-4113-9a69-1ca680ba107a&_t=gps-id%3ApcStoreLeaderboard%2Cscm-url%3A1007.22922.271278.0%2Cpvid%3A523291be-29ac-4113-9a69-1ca680ba107a%2Ctpp_buckets%3A668%232846%238109%231935&pdp_ext_f=%7B%22order%22%3A%22530%22%2C%22eval%22%3A%221%22%2C%22sceneId%22%3A%2212922%22%7D&pdp_npi=4%40dis%21USD%2186.91%2186.82%21%21%21621.22%21620.62%21%40212a6e3217490336111755062e3182%2112000045356096852%21rec%21KR%212809048098%21X&_gl=1*t35e5x*_gcl_aw*R0NMLjE3NDkwMzI3MTEuQ2p3S0NBanczZl9CQmhBUEVpd0FhQTNLNU9NMUdwMlBVVUJ5NklST0l0ejdQMGt5U2NTTnAtLWZhX2gxcjE2aEF1UGs3VlJSZFRfUGFCb0M2LU1RQXZEX0J3RQ..*_gcl_au*NzI0NzkxNTU0LjE3NDcxMTIwMTk.*_ga*NTYyNzAxMzIuMTc0NzExMjAxOQ..*_ga_VED1YSGNC7*czE3NDkwMzE5MzAkbzE0JGcxJHQxNzQ5MDMzNjA1JGo2MCRsMCRoMA..&gatewayAdapt=glo2kor
# 정상 예시 1 https://ko.aliexpress.com/item/1005006802925639.html?spm=a2g0o.store_pc_home.0.0.29326c89c2dRYi&pdp_npi=4%40dis%21USD%21US%20%2446.63%21US%20%2436.48%21%21%21333.32%21260.76%21%400baf035e17490350187532052d016c%2112000038355271009%21sh%21KR%212809048098%21X&_gl=1*1its5zs*_gcl_aw*R0NMLjE3NDkwMzI3MTEuQ2p3S0NBanczZl9CQmhBUEVpd0FhQTNLNU9NMUdwMlBVVUJ5NklST0l0ejdQMGt5U2NTTnAtLWZhX2gxcjE2aEF1UGs3VlJSZFRfUGFCb0M2LU1RQXZEX0J3RQ..*_gcl_au*NzI0NzkxNTU0LjE3NDcxMTIwMTk.*_ga*NTYyNzAxMzIuMTc0NzExMjAxOQ..*_ga_VED1YSGNC7*czE3NDkwMzE5MzAkbzE0JGcxJHQxNzQ5MDM1MDE2JGo1NSRsMCRoMA..&gatewayAdapt=glo2kor
