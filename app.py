import certifi
from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
cert = certifi.where()
client = MongoClient('Replace This With your Atlas Endpoint', tlsCAFile=cert)
db = client.dbsparta # Replace with your collection name

import jwt
import datetime
import hashlib
SECRET_KEY = 'sparta'

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"user_email": payload['email']})
        return render_template('index.html', user_name=user_info["user_name"], user_address_district=user_info["user_address_district"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/store/add')
def store_add():
    return render_template('store_add.html')

@app.route('/store/update')
def store_update():
    return render_template('store_update.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    user_email = request.form['user_email']
    user_name = request.form['user_name']
    user_pw = request.form['user_pw']
    user_address_district = request.form['user_address_district']

    pw_hash = hashlib.sha256(user_pw.encode('utf-8')).hexdigest()

    db.user.insert_one({
        'user_email': user_email,
        'user_name': user_name,
        'user_pw': pw_hash,
        'user_address_district': user_address_district
    })

    return jsonify({'status': 200, 'msg': '회원가입이 완료되었습니다.'})

@app.route('/api/email/check', methods=['GET'])
def api_email_check():
    args = request.args
    email_receive = args.get('user_email')
    user = db.user.find_one({'user_email': email_receive})
    if user is None:
        return jsonify({'status': 200, 'msg': '사용 가능한 이메일 입니다.'})
    else:
        return jsonify({'status': 400, 'msg': '이미 사용 중인 이메일 입니다.'})

@app.route('/api/name/check', methods=['GET'])
def api_nickname_check():
    args = request.args
    nickname_receive = args.get('user_name')
    user = db.user.find_one({'user_name': nickname_receive})
    if user is None:
        return jsonify({'status': 200, 'msg': '사용 가능한 닉네임 입니다.'})
    else:
        return jsonify({'status': 400, 'msg': '이미 사용 중인 닉네임 입니다.'})

@app.route('/api/login', methods=['POST'])
def api_login():
    email_receive = request.form['user_email']
    pw_receive = request.form['user_pw']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'user_email': email_receive, 'user_pw': pw_hash},{'_id':False})
    if result is not None:
        payload = {
            'email': email_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'status': 200, 'msg': '로그인이 완료되었습니다.', 'token': token})
    else:
        return jsonify({'status': 404, 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/api/store/list', methods=['GET'])
def render_store_list():
    args = request.args
    district_address = args.get('district_input')
    store_list = list(db.jason_dummy_stores.find({ 'store_address_district': district_address }, {'_id':False}))
    if len(store_list) > 0:
        return {'state': 200, 'msg': 'Successfully Fetched the data', 'data': store_list} # store_list = array containing store object
    return {'state': 404, 'msg': 'Data Not Found by Provided Key'}

@app.route("/api/store", methods=["GET"])
def get_store_post():
    store_id = request.args.get('store_id').strip()
    store_data = []
    if store_id :
        store_data = db.store.find_one({'store_id': int(store_id)}, {'_id': False})
    if store_data :
        return jsonify({'state': 200, 'data': store_data})
    else :
        return jsonify({'state': 404, 'msg': '해당하는 가맹점 정보를 찾을 수 없습니다.'})

@app.route("/api/store/post", methods=["POST"])
def add_store_post():
    store_name = request.form['store_name']
    store_address_full = request.form['store_address_full']
    store_address_district = request.form['store_address_district']
    store_address_xloc = request.form['store_address_xloc']
    store_address_yloc = request.form['store_address_yloc']
    store_label = request.form.getlist('store_label[]')

    if None not in (store_name, store_address_full, store_address_district, store_address_xloc, store_address_yloc):
        store_list = db.store.find({}, {'_id': False})
        store_id = len(list(store_list)) + 1
        db.store.insert_one(
            {
                'store_id': store_id,
                'store_name': store_name,
                'store_address_full': store_address_full,
                'store_address_district': store_address_district,
                'store_address_xloc': store_address_xloc,
                'store_address_yloc': store_address_yloc,
                'store_label': store_label
            })

    return jsonify({'msg': '가맹점 등록이 완료되었습니다.'})

@app.route("/api/store/post", methods=["PUT"])
def update_store_post():
    store_id = request.form['store_id']
    store_name = request.form['store_name']
    store_address_full = request.form['store_address_full']
    store_address_district = request.form['store_address_district']
    store_address_xloc = request.form['store_address_xloc']
    store_address_yloc = request.form['store_address_yloc']
    store_label = request.form.getlist('store_label[]')

    if None not in (store_id, store_name, store_address_full, store_address_district, store_address_xloc, store_address_yloc):
        result = db.store.update_one({'store_id': int(store_id)}, {'$set': {
                'store_name': store_name,
                'store_address_full': store_address_full,
                'store_address_district': store_address_district,
                'store_address_xloc': store_address_xloc,
                'store_address_yloc': store_address_yloc,
                'store_label': store_label
        }})
        if result.modified_count > 0 :
            return jsonify({'msg': '가맹점 정보 수정이 완료되었습니다.'})

        return jsonify({'msg': '가맹점 정보 수정이 실패했습니다.'})

@app.route("/api/store/post", methods=["DELETE"])
def delete_store_post():
    store_id = request.form['store_id']
    if store_id:
        result = db.store.delete_one({'store_id': int(store_id)})
        if result.deleted_count > 0:
            return jsonify({'msg': '가맹점 정보 삭제가 완료되었습니다.'})

        return jsonify({'msg': '가맹점 정보 삭제가 실패했습니다.'})

    return jsonify({'msg': '가맹점 정보를 찾을 수 없습니다.'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)