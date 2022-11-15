import jwt
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.oix2hts.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route("/store", methods=['GET'])
def render_store_detail():
    args = request.args
    store_id = int(args.get('store_id')) # insomnia sets the value to str by default
    store_info = db.jason_dummy_stores.find_one({'store_id':store_id},{'_id':False})

    #convert store_address_xloc and yloc to float
    store_info['store_address_xloc'] = float(store_info['store_address_xloc'])
    store_info['store_address_yloc'] = float(store_info['store_address_yloc'])

    return jsonify(store_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)