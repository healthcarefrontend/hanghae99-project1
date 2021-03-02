from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def write_review():
    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    addr_receive = request.form['addr_give']
    num_receive = request.form['num_give']
    extra_receive = request.form['extra_give']

    doc = {
        'name':name_receive,
        'count':count_receive,
        'addr':addr_receive,
        'num' : num_receive,
        'extra': extra_receive
    }
    db.mysystem.insert_one(doc)

    return jsonify({'result' : 'success', 'msg': '예약 완료!'})





@app.route('/review', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    mynotes = list(db.mysystem.find({}, {'_id': False}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'all_mynotes': mynotes})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)