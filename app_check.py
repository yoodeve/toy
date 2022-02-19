from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.q5lwb.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/check')
def clinic():
   return render_template('index_check.html')

@app.route("/check", methods=["GET"])
def movie_get():
    check_list = list(db.check.find({}, {'_id': False}))
    return jsonify({'result':check_list})

@app.route("/check-result", methods=["GET"])
def movie_get():
    check-result_list = list(db.check-result.find({}, {'_id': False}))
    return jsonify({'result':check-result_list})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5050,debug=True)

doc = [
   {'num':1,'age':21}
]
db.users.insert_one(doc)