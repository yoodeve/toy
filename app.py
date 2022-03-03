from flask import Flask, render_template, jsonify
from selenium import webdriver

from pymongo import MongoClient
client = MongoClient('mongodb+srv://janhold:sparta@cluster0.vyplo.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

from selenium.webdriver.chrome.service import Service
app = Flask(__name__)
s = Service('/Users/yoo/Desktop/yoo/projects/toy_clinic/chromedriver')

driver = webdriver.Chrome(service=s)

@app.route('/clinics')
def clinic():
    return render_template('index_clinic.html')


@app.route("/clinic", methods=["GET"])
def clinic_get():
    clinic_list = list(db.clinics.find({}, {'_id': False}))
    return jsonify({'clinics': clinic_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)
