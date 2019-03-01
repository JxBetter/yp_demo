import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/<aid>')
def index(aid):
    return render_template('xwyz.html', appid=aid)


@app.route('/back', methods=['POST'])
def back():
    print(request.form)
    return jsonify({'code': 0, 'msg': 'ok'})

if __name__ == '__main__':
    app.run()