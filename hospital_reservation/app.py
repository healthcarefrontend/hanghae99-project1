from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

import jwt
import datetime
import hashlib
from datetime import datetime, timedelta

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
        'name': name_receive,
        'count': count_receive,
        'addr': addr_receive,
        'num': num_receive,
        'extra': extra_receive
    }
    db.mysystem.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '예약 완료!'})


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
def check_dup2():
    num_receive = request.form['num_give']
    addr_receive = request.form['addr_give']

    # exists = bool(db.mysystem.find({
    #                                     '$ and' :[
    #                                         {"addr": addr_receive}, {"num": num_receive}
    #                                     ]
    #                                 }))

    exists = bool(db.mysystem.find_one({"addr": addr_receive, "num": num_receive}))

    # exists = bool(db.mysystem.find_one({"num": num_receive}))
    return jsonify({'result': 'success', 'exists': exists})


###################################################################################
###############################유훈님 코드###################################

####### 회원가입에서 전달한 정보 받는 API####################
########################################################
########################################################

@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'pw': pw_receive
    }
    db.mysystem.insert_one(doc)  # db를 users에 insert 함. (doc를 - 생성된 딕셔너리)
    return jsonify({'result': 'success', 'msg': '회원가입 실패'})


####### id중복확인 서버단 API#############################
########################################################
########################################################

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    user_id_receive = request.form['user_id_give']
    exists = bool(db.mysystem.find_one({"id_receive": user_id_receive}))
    return jsonify({'result': 'success', 'exists': 'exist'})


####회원가입 시 서버단 API#######################################
##############################################################
##############################################################

@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['user_id_give']
    password_receive = request.form['user_pw_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    doc = {
        "id": username_receive,  # 아이디
        "pw": password_hash,  # 비밀번호
    }
    db.mysystem.insert_one(doc)
    return jsonify({'result': 'success'})


###################################################################################
###############################유훈님 코드###################################
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': username_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
