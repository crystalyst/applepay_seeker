import jwt
import requests
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.oix2hts.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/test', methods=['GET'])
def map_test():
    return render_template('mainpage.html')

@app.route('/store/map', methods=['POST'])
def map_by_district():
    district_receive = request.form['address_district_give']
    return jsonify({'district':district_receive})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)