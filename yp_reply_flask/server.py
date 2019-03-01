import json
import urllib.parse
import pymysql
from flask import Flask, request

app = Flask(__name__)
connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='gujinxin',
    db='yp_callback',
    charset='utf8'
)
cursor = connect.cursor()

@app.route('/', methods=['POST'])
def index():
	print(request.headers)
	reply_data = request.form.get('sms_reply')
	reply_dict = json.loads(urllib.parse.unquote(reply_data))
	sql = 'INSERT INTO mesage_reply (mobile, reply_time, text) VALUES ( "{}", "{}", "{}" )'.format(reply_dict.get('mobile'), reply_dict.get('reply_time'), reply_dict.get('text'))
	print(sql)
	cursor.execute(sql)
	connect.commit()
	return '0'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9996)
