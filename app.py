from flask import Flask, render_template

app = Flask(__name__)

@app.route('/clinic')
def clinic():
    return render_template('index_clinic.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)
