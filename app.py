import jwt
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.oix2hts.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route("/store", methods=['GET'])
def render_store_detail():
    args = request.args
    store_id = args.get('store_id')

    store_info = db.jason_dummy_stores.find_one({'store_id':store_id},{'_id':False})
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)