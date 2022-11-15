import jwt
import certifi
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
cert = certifi.where()
client = MongoClient('mongodb+srv://yjsohn:sparta@cluster0.v3x09yn.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=cert)
db = client.dbapplepay_test

@app.route("/store/post", methods=["POST"])

def add_store_post():
    data = request.get_json()
    store_name = data['store_name']
    store_address_full = data['store_address_full']
    store_address_district = data['store_address_district']
    store_address_xloc = data['store_address_xloc']
    store_address_yloc = data['store_address_yloc']
    store_label = data['store_label']

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

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)