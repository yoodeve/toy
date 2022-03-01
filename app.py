from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://copa:copa@cluster0.dmead.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/clinic')
def clinic():
    return render_template('index_clinic.html')

@app.route('/check_list')
def check_list():
    return render_template('index_check.html')

@app.route("/check", methods=["GET"])
def check_get():
    symp_list = list(db.check.find({}, {'_id': False}))
    return jsonify({'symps': symp_list})

@app.route("/result", methods=["GET"])
def result_get():
    result_list = list(db.result.find({}, {'_id': False}))
    return jsonify({'results': result_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)