import jwt
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('Replace This With your Atlas Endpoint')
db = client.dbsparta # replace this with your document name

@app.route('/api/user', methods=['GET'])
def render_user_data_by_id():
    args = request.args
    try:
        user_id = int(args.get('user_id'))
        user_doc = db.jason_dummy_users.find_one({ 'user_id': user_id }, {'_id': False})
        return {'state': 200, 'msg': 'User Data Successfully Fetched!', 'data': user_doc}

    except TypeError:
        return {'state': 400, 'msg': 'No user_id key provided'}
    except ValueError:
        return {'state': 400, 'msg': 'Invalid Input or No Such User'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)