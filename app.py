from flask import Flask, request, jsonify
import certifi

app = Flask(__name__)

from pymongo import MongoClient
cert = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.oix2hts.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=cert)
db = client.dbsparta

@app.route("/store", methods=["GET"])

def get_store_post():
    store_id = request.args.get('store-id').strip()
    store_data = []
    if store_id :
        store_data = db.store.find_one({'store_id': int(store_id)}, {'_id': False})
    if store_data :
        return jsonify(store_data)
    else :
        return jsonify({'msg': 'data not found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)