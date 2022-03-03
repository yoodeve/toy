from flask import Flask, render_template, jsonify, request
import requests

# 25개구 for문으로 돌려서 카페 정보 크롤링하기

import os
from time import sleep
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from pymongo import MongoClient
client = MongoClient('mongodb+srv://janhold:sparta@cluster0.vyplo.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
app = Flask(__name__)
s = Service('/Users/yoo/Desktop/yoo/projects/toy_clinic/chromedriver')

driver = webdriver.Chrome(service=s)

@app.route('/clinic')
def clinic():
    return render_template('index_clinic.html')

@app.route("/clinic/find", methods=["POST"])
def clinic_post():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    hour_receive = request.form['hour_give']
    tel_receive = request.form['tel_give']
# 전국 시 도
    loc_list = ['서울', '경기도', '충북', '충남', '전북', '전남', '경북', '경남', '걍원도', '제주']

    # csv 파일에 헤더 만들어 주기
    for index, loc_name in enumerate(loc_list):
        fileName = 'test.csv'
        file = open(fileName, 'w', encoding='utf-8')

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36   ")
        options.add_argument('lang=ko_KR')
        chromedriver_path = "/Users/yoo/Desktop/yoo/projects/toy_clinic/chromedriver"
        driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)  # chromedriver 열기
        driver.get('https://map.kakao.com/')  # 주소 가져오기
        search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')  # 검색 창
        search_area.send_keys(loc_name + ' 선별진료소')  # 검색어 입력
        driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
        driver.implicitly_wait(3)  # 기다려 주자
        more_page = driver.find_element_by_id("info.search.place.more")
        # more_page.click()
        more_page.send_keys(Keys.ENTER)  # 더보기 누르고
        # 첫 번째 검색 페이지 끝
        # driver.implicitly_wait(5) # 기다려 주자
        time.sleep(1)

        # next 사용 가능?
        next_btn = driver.find_element_by_id("info.search.page.next")
        has_next = "disabled" not in next_btn.get_attribute("class").split(" ")
        Page = 1
        while has_next:  # 다음 페이지가 있으면 loop
            # for i in range(2, 6): # 2, 3, 4, 5
            file = open(fileName, 'a', encoding='utf-8')
            time.sleep(1)
            # place_lists = driver.find_elements_by_css_selector('#info\.search\.place\.list > li:nth-child(1)')
            # 페이지 루프
            # info\.search\.page\.no1 ~ .no5
            page_links = driver.find_elements_by_css_selector("#info\.search\.page a")
            pages = [link for link in page_links if "HIDDEN" not in link.get_attribute("class").split(" ")]
            # print(len(pages), "개의 페이지 있음")
            # pages를 하나씩 클릭하면서
            for i in range(1, 6):
                xPath = '//*[@id="info.search.page.no' + str(i) + '"]'
                try:
                    page = driver.find_element_by_xpath(xPath)
                    page.send_keys(Keys.ENTER)
                except ElementNotInteractableException:
                    print('End of Page')
                    break;
                sleep(3)
                place_lists = driver.find_elements_by_css_selector('#info\.search\.place\.list > li')
                for p in place_lists:  # WebElement
                    # print(p.get_attribute('innerHTML'))
                    # print("type of p:", type(p))
                    store_html = p.get_attribute('innerHTML')
                    store_info = BeautifulSoup(store_html, "html.parser")
                    # BS -> 분석
                    #
                    request.form['name_give'] = str(store_info.select('.head_item > .tit_name > .link_name'))
                    request.form['address_give'] = str(store_info.select('.info_item > .addr > p'))
                    request.form['hour_give'] = str(store_info.select('.info_item > .openhour > p > a'))
                    request.form['tel_give'] = str(store_info.select('.info_item > .contact > span'))
                    # print("length:", len(place_name))
                    if len(name_receive) == 0:
                        continue  # 광고
                    request.form['name_give'] = store_info.select('.head_item > .tit_name > .link_name')[0].text
                    request.form['address_give'] = store_info.select('.info_item > .addr > p')[0].text
                    request.form['hour_give'] = store_info.select('.info_item > .openhour > p > a')[0].text
                    request.form['tel_give'] = store_info.select('.info_item > .contact > span')[0].text

                    # 사진url 수집
                    detail = p.find_element_by_css_selector('div.info_item > div.contact > a.moreview')
                    detail.send_keys(Keys.ENTER)

                    driver.switch_to.window(driver.window_handles[-1])

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    print(request.form['name_give'], request.form['address_give'], request.form['hour_give'],
                          request.form['tel_give'])

            if not has_next:
                print('Arrow is Disabled')
                driver.close()
                file.close()
                break  # 다음 페이지 없으니까 종료
            else:  # 다음 페이지 있으면
                Page += 1
                next_btn.send_keys(Keys.ENTER)

            doc = {
                'name': name_receive,
                'address': address_receive,
                'hour': hour_receive,
                'tel': tel_receive,
            }
            db.clinics.insert_one(doc)

@app.route("/clinic/read", methods=["GET"])
def clinic_get():
    clinic_list = list(db.clinics.find({}, {'_id': False}))
    return jsonify({'clinics': clinic_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)
