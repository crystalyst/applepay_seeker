import jwt
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.oix2hts.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/store/comment', methods=['POST'])
def add_comment():
    store_id = int(request.form['store_id'])
    # user_id will be included in the session/cookie - temp
    user_id = int(request.form['user_id'])
    content = request.form['content']

    comment_doc = {
        'user_id': user_id,
        'store_id': store_id,
        'content': content
    }
    db.jason_dummy_comments.insert_one(comment_doc)

    return {'result': 'success'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)