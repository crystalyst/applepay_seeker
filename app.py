import jwt
import certifi
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
cert = certifi.where()
client = MongoClient('mongodb+srv://yjsohn:sparta@cluster0.v3x09yn.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=cert)
db = client.dbapplepay_test

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/store/add')
def store_add():
    return render_template('store_add.html')
@app.route("/api/store/post", methods=["POST"])

def add_store_post():
    print(request.form)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)