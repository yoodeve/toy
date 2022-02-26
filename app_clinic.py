from flask import Flask, render_template, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://janhold:sparta@cluster0.vyplo.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/clinic')
def clinic():
   return render_template('index_clinic.html')

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.kkoMap.find({}, {'_id': False}))
    return jsonify({'maps':map_list})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5050,debug=True)