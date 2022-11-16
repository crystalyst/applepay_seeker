from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('Replace with your Atlas Endpoint')
db = client.dbsparta # Replace with your collection name

@app.route('/api/user/store/list', methods=['GET'])
def render_store_list_per_user():
    args = request.args
    try:
        user_id = int(args.get('user_id')) # avoid KeyError
        # Your collection name -> change it to applicable collection name!
        user_doc = db.jason_dummy_users.find_one({'user_id': user_id}, {'_id': False})
        store_list_per_user = user_doc.get('user_post')  # to avoid KeyError if user_post DNE

        if len(store_list_per_user) > 0:
            return {'state': 200, 'msg': 'Successfully Fetched the data',
                    'data': store_list_per_user}  # store_list = array containing store object
        return {'state': 404, 'msg': 'Data Not Found by Provided Key'}  # empty array
    except TypeError: # exception handling just in case args.get('user_id') takes None or non-string value
        return {'state': 400, 'msg': 'Bad Request - Invalid Input from client or no such user exists'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)