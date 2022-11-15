import certifi
from flask import Flask, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
cert = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.oix2hts.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=cert)
db = client.dbsparta

@app.route("/store/post", methods=["POST"])

def add_store_post():
    store_name = request.form['store_name']
    store_address_full = request.form['store_address_full']
    store_address_district = request.form['store_address_district']
    store_address_xloc = request.form['store_address_xloc']
    store_address_yloc = request.form['store_address_yloc']
    store_label = request.form.getlist(['store_label[]'])

    if None not in (store_name, store_address_full, store_address_district, store_address_xloc, store_address_yloc):
        store_list = db.store.find({}, {'_id': False})
        store_id = len(list(store_list)) + 1
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
        if result.inserted_count > 0:
            return jsonify({'msg': '가맹점 정보 추가가 완료되었습니다.'})

    return jsonify({'msg': '가맹점 정보 추가가 실패했습니다.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)