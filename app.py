from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('Replace with your Atlas Endpoint')
db = client.dbsparta # Replace with your collection name

@app.route('/api/store/list', methods=['GET'])
def render_store_list():
    args = request.args
    district_address = args.get('district_input')
    store_list = list(db.jason_dummy_stores.find({ 'store_address_district': district_address }, {'_id':False}))
    if len(store_list) > 0:
        return {'state': 200, 'msg': 'Successfully Fetched the data', 'data': store_list} # store_list = array containing store object
    return {'state': 404, 'msg': 'Data Not Found by Provided Key'} # empty array

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)