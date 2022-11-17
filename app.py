import certifi
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient

cert = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.oix2hts.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

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
        return render_template('index.html', user_name=user_info["user_name"],
                               user_address_district=user_info["user_address_district"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("render_login_page", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("render_login_page", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def render_login_page():
    return render_template('login.html')


@app.route('/user')
def render_user_page():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"user_email": payload['email']})
        if user_info:
            return render_template('user.html', user_id=user_info["user_id"], user_name=user_info["user_name"],
                                   user_email=user_info["user_email"],
                                   user_address_district=user_info["user_address_district"])
        return redirect(url_for("render_login_page", msg="존재하지 않는 사용자입니다."))
    except jwt.ExpiredSignatureError:
        return redirect(url_for("render_login_page", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("render_login_page", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/store/add')
def render_store_add_page():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"user_email": payload['email']})
        if user_info:
            return render_template('store_add.html', user_id=user_info["user_id"], user_name=user_info["user_name"],
                                   user_address_district=user_info["user_address_district"])
        return redirect(url_for("render_login_page", msg="존재하지 않는 사용자입니다."))
    except jwt.ExpiredSignatureError:
        return redirect(url_for("render_login_page", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("render_login_page", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/store/update')
def render_store_update_page():
    return render_template('store_update.html')


@app.route('/api/register', methods=['POST'])
def api_register():
    user_email = request.form['user_email']
    user_name = request.form['user_name']
    user_pw = request.form['user_pw']
    user_address_district = request.form['user_address_district']

    user_list = list(db.user.find({'user_id': True}, {'_id': False}))
    if user_list:
        user_id_sorted = sorted(list(user_list), key=lambda user: user['user_id'])
        user_id = user_id_sorted[-1]['store_id'] + 1
    else:
        user_id = 1

    pw_hash = hashlib.sha256(user_pw.encode('utf-8')).hexdigest()

    db.user.insert_one({
        'user_id': user_id,
        'user_email': user_email,
        'user_name': user_name,
        'user_pw': pw_hash,
        'user_address_district': user_address_district,
        'user_post': [],
        'user_like': []
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
    result = db.user.find_one({'user_email': email_receive, 'user_pw': pw_hash}, {'_id': False})
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
    store_list = list(db.store.find({'store_address_district': district_address}, {'_id': False}))
    if len(store_list) > 0:
        return {'state': 200, 'data': store_list}  # store_list = array containing store object
    return {'state': 404, 'msg': '사용자가 등록한 가맹점 정보를 불러올 수 없습니다.'}


@app.route("/api/store", methods=["GET"])
def get_store_post():
    store_id = request.args.get('store_id').strip()
    store_data = []
    if store_id:
        store_data = db.store.find_one({'store_id': int(store_id)}, {'_id': False})
    if store_data:
        return jsonify({'state': 200, 'data': store_data})
    else:
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
        store_list = db.store.find({}, {'store_id': True, '_id': False})
        if store_list:
            store_id_sorted = sorted(list(store_list), key=lambda store: store['store_id'])
            store_id = store_id_sorted[-1]['store_id'] + 1
        else:
            store_id = 1

        result = db.store.insert_one(
            {
                'store_id': store_id,
                'store_name': store_name,
                'store_address_full': store_address_full,
                'store_address_district': store_address_district,
                'store_address_xloc': store_address_xloc,
                'store_address_yloc': store_address_yloc,
                'store_label': store_label
            })
        if result.inserted_id:
            return jsonify({'status': 200, 'msg': '가맹점 정보 추가가 완료되었습니다.'})

    return jsonify({'status': 200, 'msg': '가맹점 정보 추가가 실패했습니다.'})


@app.route("/api/store/post", methods=["PUT"])
def update_store_post():
    store_id = request.form['store_id']
    store_name = request.form['store_name']
    store_address_full = request.form['store_address_full']
    store_address_district = request.form['store_address_district']
    store_address_xloc = request.form['store_address_xloc']
    store_address_yloc = request.form['store_address_yloc']
    store_label = request.form.getlist('store_label[]')

    if None not in (
            store_id, store_name, store_address_full, store_address_district, store_address_xloc, store_address_yloc):
        result = db.store.update_one({'store_id': int(store_id)}, {'$set': {
            'store_name': store_name,
            'store_address_full': store_address_full,
            'store_address_district': store_address_district,
            'store_address_xloc': store_address_xloc,
            'store_address_yloc': store_address_yloc,
            'store_label': store_label
        }})
        if result.modified_count > 0:
            return jsonify({'status': 200, 'msg': '가맹점 정보 수정이 완료되었습니다.'})

        return jsonify({'status': 500, 'msg': '가맹점 정보 수정이 실패했습니다.'})


@app.route("/api/store/post", methods=["DELETE"])
def delete_store_post():
    store_id = request.form['store_id']
    if store_id:
        result = db.store.delete_one({'store_id': int(store_id)})
        if result.deleted_count > 0:
            return jsonify({'status': 200, 'msg': '가맹점 정보 삭제가 완료되었습니다.'})

        return jsonify({'status': 500, 'msg': '가맹점 정보 삭제가 실패했습니다.'})

    return jsonify({'status': 404, 'msg': '가맹점 정보를 찾을 수 없습니다.'})


@app.route('/api/store/map', methods=['POST'])
def map_by_district():
    district_receive = request.form.get('address_district_give')
    return jsonify({'district': district_receive})


@app.route('/api/user', methods=['GET'])
def render_user_data_by_id():
    args = request.args
    try:
        user_id = int(args.get('user_id'))
        user_doc = db.user.find_one({'user_id': user_id}, {'_id': False})
        return {'state': 200, 'data': user_doc}
    except TypeError:
        return {'state': 400, 'msg': '잘못된 사용자 ID 타입 입니다.'}
    except ValueError:
        return {'state': 400, 'msg': '잘못된 사용자 정보이거나 없는 사용자 정보 입니다.'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
