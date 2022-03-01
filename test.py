# 반올림 처리
from math import ceil
#DB 연결
from pymongo import MongoClient
client = MongoClient('mongodb+srv://copa:copa@cluster0.dmead.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

#서버
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

#home 화면
@app.route('/')
def home():
    return render_template('dashboard.html')

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
   app.run('0.0.0.0', port=5000, debug=True)
