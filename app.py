import jwt
from flask import Flask, render_template, request, jsonify, url_for, 
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.oix2hts.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)