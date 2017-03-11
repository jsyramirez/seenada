import hashlib
from flask import Flask,request,jsonify,abort
from DbAccess import DbAccess

app = Flask(__name__)
db = DbAccess()

# basic homepage
@app.route('/')
def home():
    return "Welcome to the page"

@app.route('/signup', methods=['POST'])
def sign_up():
    print "we got here"
    content = request.get_json(force=True)
    print content
    username = content['username']
    password = content['password']
    hashed_password = hashlib.sha512(password).hexdigest()
    db.insert_user(username, hashed_password) 
    return "added"

@app.route('/signin', methods=['POST'])
def signin():
    content = request.get_json(force=True)
    username = content['username']
    password = content['password']
    hash_password = hashlib.sha512(password).hexdigest()
    result = db.get_user(username)
    if result is None:
        abort(403)
    else:
        if result[1] != hash_password:
            abort(403)
        else:
            return "sign in successfully"    

@app.route('/send_message', methods=['POST'])
def send_message():
    content = request.get_json(force=True)
    response = db.insert_message(content)
    if response == 'success':
        return response
    else:
        print response
        abort(500)

@app.route('/get_message', methods=['POST'])
def get_message():
    content = request.get_json(force=True)
    username = content['username']
    password = content['password']
    rows = db.get_message(username)
    messages = []
    for row in rows:
        message = {}
        message['from'] = row[1]
        message['content'] = row[3]
        message['timestamp'] = row[5]
        messages.append(message)
    return jsonify(messages)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

