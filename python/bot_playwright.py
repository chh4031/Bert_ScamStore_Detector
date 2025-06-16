from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=True이면 CAPTCHA 나올 수 있음
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        locale="en-US"
    )
    page = context.new_page()
    page.goto("https://ko.aliexpress.com/item/1005008486195215.html?spm=a2g0o.store_pc_home.0.0.24d0433avJPLsh&gps-id=pcStoreLeaderboard&scm=1007.22922.271278.0&scm_id=1007.22922.271278.0&scm-url=1007.22922.271278.0&pvid=523291be-29ac-4113-9a69-1ca680ba107a&_t=gps-id%3ApcStoreLeaderboard%2Cscm-url%3A1007.22922.271278.0%2Cpvid%3A523291be-29ac-4113-9a69-1ca680ba107a%2Ctpp_buckets%3A668%232846%238109%231935&pdp_ext_f=%7B%22order%22%3A%22530%22%2C%22eval%22%3A%221%22%2C%22sceneId%22%3A%2212922%22%7D&pdp_npi=4%40dis%21USD%2186.91%2186.82%21%21%21621.22%21620.62%21%40212a6e3217490336111755062e3182%2112000045356096852%21rec%21KR%212809048098%21X&_gl=1*t35e5x*_gcl_aw*R0NMLjE3NDkwMzI3MTEuQ2p3S0NBanczZl9CQmhBUEVpd0FhQTNLNU9NMUdwMlBVVUJ5NklST0l0ejdQMGt5U2NTTnAtLWZhX2gxcjE2aEF1UGs3VlJSZFRfUGFCb0M2LU1RQXZEX0J3RQ..*_gcl_au*NzI0NzkxNTU0LjE3NDcxMTIwMTk.*_ga*NTYyNzAxMzIuMTc0NzExMjAxOQ..*_ga_VED1YSGNC7*czE3NDkwMzE5MzAkbzE0JGcxJHQxNzQ5MDMzNjA1JGo2MCRsMCRoMA..&gatewayAdapt=glo2kor")

    time.sleep(5)  # 페이지 로딩 대기
    print("페이지 제목:", page.title())

    # 웹사이트에서 navigator.webdriver 상태 확인
    webdriver_flag = page.evaluate("() => navigator.webdriver")
    print("navigator.webdriver:", webdriver_flag)  # None이면 우회 성공

    # 예: '초이스' 요소 가져오기 (해당 요소가 있다면)
    try:
        choice_text = page.locator('.choice-mind--box--fJKH05M span').text_content(timeout=5000)
        print("초이스 정보:", choice_text)
    except Exception as e:
        print("초이스 정보 가져오기 실패:", e)

    browser.close()