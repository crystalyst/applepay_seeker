import jwt
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.oix2hts.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route("/store/like", methods=['POST'])
def like_store():
    store_id = request.form['store_id']
    # user_id will be obtained from cookie - below is for testing purpose
    user_id = int(request.form['user_id'])
    user_doc = db.jason_dummy_users.find_one({'user_id':user_id}, {'_id':False})
    print(user_doc)
    current_like_list = user_doc['user_like']
    store_doc = db.jason_dummy_stores.find_one({'store_id':store_id}, {'_id':False})
    store_like_total = store_doc['store_like']
    if store_id not in current_like_list:
        current_like_list.append(store_id)
        store_like_total += 1
    else:
        current_like_list.remove(store_id)
        store_like_total -= 1

    db.jason_dummy_users.update_one({'user_id': user_id}, {'$set': {'user_like': current_like_list}})
    db.jason_dummy_stores.update_one({'store_id': store_id}, {'$set': {'store_like': store_like_total}})

    return {'result': 'test okay'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)