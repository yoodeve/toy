
# =======
from math import ceil

from flask import Flask, render_template, jsonify, request

from config import MONGODB_SETTIING

app = Flask(__name__)

# DB연결
from pymongo import MongoClient
db = MongoClient(MONGODB_SETTIING.values())

# 크롤링
import requests
from bs4 import BeautifulSoup

@app.route('/')
def Dashboard():
    return render_template('index.html')

@app.route('/clinic')
def clinic():
    return render_template('index_clinic.html')

@app.route("/clinic", methods=["GET"])
def clinic_get():
    clinic_list = list(db.clinics.find({}, {'_id': False}))
    return jsonify({'clinics': clinic_list})

@app.route('/check_list')
def check_list():
    return render_template('index_check.html')

@app.route("/check", methods=["GET"])
def check_get():
    symp_list = list(db.check.find({}, {'_id': False}))
    return jsonify({'symps': symp_list})

@app.route('/chart')
def chart_home():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    data_city = requests.get(
        'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=',
        headers=headers)

    soup_city = BeautifulSoup(data_city.text, 'html.parser')

    cities = soup_city.select('#content > div > div.data_table.midd.mgt24 > table > tbody > tr')

    for city in cities:
        city_name = city.select_one('th').text
        city_domes = city.select_one('td:nth-child(3)').text
        city_intl = city.select_one('td:nth-child(4)').text
        city_subtotal = city.select_one('td:nth-child(2)').text
        city_total = city.select_one('td:nth-child(5)').text
        city_death = city.select_one('td:nth-child(6)').text

        # charts_city DB에 처음 설정
        # doc = {'city_name': city_name,
        #        'city_domes': city_domes,
        #        'city_intl': city_intl,
        #        'city_subtotal': city_subtotal,
        #        'city_total': city_total,
        #        'city_death': city_death}
        # db.charts_city.insert_one(doc)

        db.charts_city.update_one({'city_name': city_name},
                                  {'$set': {'city_domes': city_domes, 'city_intl': city_intl,
                                            'city_subtotal': city_subtotal, 'city_total': city_total,
                                            'city_death': city_death}})

    data = requests.get(
        'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun=',
        headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    charts = soup.select('#content > div > div:nth-child(14) > table > tbody > tr:nth-child(1)')
    for chart in charts:
        dailytotal_1 = chart.select_one('td:nth-child(2)').text
        dailytotal_2 = chart.select_one('td:nth-child(3)').text
        dailytotal_3 = chart.select_one('td:nth-child(4)').text
        dailytotal_4 = chart.select_one('td:nth-child(5)').text
        dailytotal_5 = chart.select_one('td:nth-child(6)').text
        dailytotal_6 = chart.select_one('td:nth-child(7)').text
        dailytotal_7 = chart.select_one('td:nth-child(8)').text

    dates = soup.select('#content > div > div:nth-child(14) > table > thead > tr')
    for date in dates:
        date_1 = date.select_one('th:nth-child(2)').text
        date_2 = date.select_one('th:nth-child(3)').text
        date_3 = date.select_one('th:nth-child(4)').text
        date_4 = date.select_one('th:nth-child(5)').text
        date_5 = date.select_one('th:nth-child(6)').text
        date_6 = date.select_one('th:nth-child(7)').text
        date_7 = date.select_one('th:nth-child(8)').text

    doc1 = {'daily_today': date_1, 'daily_total': dailytotal_1}
    doc2 = {'daily_today': date_2, 'daily_total': dailytotal_2}
    doc3 = {'daily_today': date_3, 'daily_total': dailytotal_3}
    doc4 = {'daily_today': date_4, 'daily_total': dailytotal_4}
    doc5 = {'daily_today': date_5, 'daily_total': dailytotal_5}
    doc6 = {'daily_today': date_6, 'daily_total': dailytotal_6}
    doc7 = {'daily_today': date_7, 'daily_total': dailytotal_7}

    docs = [doc1, doc2, doc3, doc4, doc5, doc6, doc7]
    dates = [date_1, date_2, date_3, date_4, date_5, date_6, date_7]

    for doc, date in zip(docs, dates):
        def check_coroutine():
            x = None
            existing = db.charts.find_one({'daily_today': date})

            while True:
                x = (yield x)
                if existing == None:
                    x = db.charts.insert_one(doc)
                    # print(date,'저장완료')

                else:
                    pass
                    # print('저장X')

        co = check_coroutine()
        next(co)

        for i in range(1):
            co.send(i)

        # co.close()
        # print(doc)
    return render_template('index_chart.html')

@app.route("/chart/list", methods=["GET"])
def show_chart():
    chart_list = list(db.charts.find({}, {'_id': False}))
    return jsonify({'charts': chart_list})

@app.route("/chart/city", methods=["POST","GET"])
def city_show():
    if request.method == "POST":
        city_receive = request.form['city_give']
        db.charts_tempcity.drop()

        find_city = db.charts_city.find_one({'city_name': city_receive})
        db.charts_tempcity.insert_one(find_city)
        print('post', db.charts_city.find_one({'city_name': city_receive}))
        return jsonify({})

    elif request.method == "GET":
        get_city = list(db.charts_tempcity.find({}, {'_id': False}))
        print('get', get_city)
        return jsonify({'city_name': get_city})


#백신후기 page
@app.route('/review')
def review():
    return render_template('review.html')

#백신후기 작성
@app.route("/toy", methods=["POST"])
def web_toy_post():
    writer_receive = request.form['writer_give']
    review_receive = request.form['review_give']

    doc = {
        'writer':writer_receive,
        'review':review_receive,
    }
    db.vaccine.insert_one(doc)

    return jsonify({'msg':'후기작성 완료!'})

#백신후기 작성
@app.route("/toy", methods=["GET"])
def web_toy_get():

    review_list = list(db.vaccine.find({}, {'_id': False}))

    return jsonify({'reviews': review_list})

#네이버 백신 종류별 후기
@app.route("/naver", methods=["GET"])
def web_naver_get():
    page = request.args.get("page", 1, type=int)
    # btype 1=화이자, 2=모더나, 3=아스트라, 4=얀센
    btype = request.args.get("btype", 1, type=int)
    search = "화이자백신후유증 "

    print(page)
    print(btype)
    if (btype==2):
        search = "모더나백신후유증 "
    elif (btype==3):
        search = "아스트라제네카백신후유증 "
    elif (btype==4):
        search = "얀센백신후유증 "

    view_list = list(db.naver_view.find({'search': search}, {'_id': False}).skip((page - 1) * 5).limit(5))
    count = len(list(db.naver_view.find({'search': search}, {'_id': False})))
    last_page = ceil(count / 5)

    return jsonify({'view_list': view_list, 'last_page': last_page})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)

# >>>>>>> c188acabc8f4563a12f39946f78b9c47f32c10d7
