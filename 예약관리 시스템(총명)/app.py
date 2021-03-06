from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

###########################################################
########### 예약한 데이터들 DB에 입력 API (총명)
###########################################################

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

###########################################################
########### DB에서 예약 정보 모두 가져오기 API (총명)
###########################################################


@app.route('/review', methods=['GET'])
def read_reviews():
    mynotes = list(db.mysystem.find({}, {'_id': False}))
    return jsonify({'all_mynotes': mynotes})


###########################################################
###########  진료시간 예약 중복체크 API (총명)
###########################################################

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    num_receive = request.form['num_give']
    addr_receive = request.form['addr_give']

    # exists = bool(db.mysystem.find({
    #                                     '$ and' :[
    #                                         {"addr": addr_receive}, {"num": num_receive}
    #                                     ]
    #                                 }))

    exists = bool(db.mysystem.find_one({"addr": addr_receive, "num": num_receive}))

    #exists = bool(db.mysystem.find_one({"num": num_receive}))
    return jsonify({'result': 'success', 'exists': exists})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)