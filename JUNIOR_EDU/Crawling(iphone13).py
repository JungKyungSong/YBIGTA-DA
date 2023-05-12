from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  # 크롬드라이버 자동업데이트
from selenium.common.exceptions import NoSuchElementException
import time
import openpyxl

#Workbook 생성
wb = openpyxl.Workbook()

#Sheet 활성
sheet = wb.active

# 4. 데이터프레임 내 header(변수명)생성
sheet.append(["순위", "상품명", "가격", "상세페이지"])

service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

# 웹페이지 주소 이동
browser.get("https://search.shopping.naver.com/search/all?query=%EC%95%84%EC%9D%B4%ED%8F%B013&cat_id=&frm=NVSHATC")
time.sleep(2)

#browser.find_element(By.CSS_SELECTOR, 'a.nav.shop').click()
#time.sleep(1)

#검색창 찾기 = 클릭
#search = browser.find_element(By.CSS_SELECTOR, 'input.co_srh_input._input').click()

#검색어 입력
#search.send_keys('아이폰13')
#search.send_keys(Keys.ENTER)
#time.sleep(3)

# 스크롤 전 높이
before_h = browser.execute_script("return window.scrollY") #execute_script = 자바스크립트 명령어 실행

# 무한 스크롤 - 반복문
while True:
    # 맨 아래로 스크롤을 내린다. body = 모든 웹사이트에 존재
    # 키보드의 END키 누르면 웹페이지 맨아래로 이동
    browser.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)
    time.sleep(1) # 스크롤 사이 페이지 로딩시간
    after_h = browser.execute_script("return window.scrollY")

    if after_h == before_h:
        break
    before_h = after_h  # 스크롤 후 높이가 다르면 before_h를 업데이트

items = browser.find_elements(By.CSS_SELECTOR, 'li.basicList_item__2XT81')

i = 1
for item in items:
    try:
        ex = item.find_element(By.CSS_SELECTOR, 'span.thumbnail_sale__T-L2g').text
        continue
    except NoSuchElementException:
        name = item.find_element(By.CSS_SELECTOR, 'div.basicList_title__3P9Q7').text
        price = item.find_element(By.CSS_SELECTOR, 'span.price_num__2WUXn').text
        link = item.find_element(By.CSS_SELECTOR, 'div > a.basicList_link__1MaTN').get_attribute('href')
        # sheet 내 각 행에 데이터 추가
        sheet.append([i, name, price, link])
        i += 1

# 수집한 데이터 저장
wb.save(filename='iphone13_crawling.xlsx')


