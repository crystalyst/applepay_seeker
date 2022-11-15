from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.oix2hts.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/store/list', methods=['GET'])
def render_store_list():
    args = request.args
    district_address = args.get('user_address_district')
    trimmed_address = district_address[1:-1]
    store_list = list(db.jason_dummy_stores.find({ 'store_address_district': trimmed_address },{'_id':False}))

    return store_list

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)