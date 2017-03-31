#!/usr/bin/env python
'''api for secured chat application'''
import hmac
import hashlib
import time
import uuid
import binascii
import logging
from flask import Flask, request, jsonify, abort
import scrypt
import jwt
from DbAccess import DbAccess

LOGGER = logging.getLogger("api")
LOGGER.setLevel(logging.INFO)
HANDLER = logging.FileHandler('/var/log/seenada/api.log')
HANDLER.setLevel(logging.INFO)
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

APP = Flask(__name__)
DB = DbAccess()

@APP.route("/")
def hello():
    '''basic homepage for testing'''
    return "Hello. Welcome"

@APP.route("/register", methods=['POST'])
def register():
    '''new user sign up'''
    content = request.get_json(force=True)
    username = (content['username']).encode('ascii', 'ignore')
    pwd = (content['password']).encode('ascii', 'ignore')
    salt = uuid.uuid4().hex
    hashed_binary_pwd = scrypt.hash(pwd, salt)
    hashed_pwd = binascii.hexlify(hashed_binary_pwd)
    response = DB.add_user(username, salt, hashed_pwd)
    if response == 'ok':
        return "Added successfully"
    else:
        LOGGER.error(response)
        abort(500)

@APP.route("/signin1", methods=['POST'])
def first_signin():
    '''first signin, return salt'''
    content = request.get_json(force=True)
    username = content['username']
    user = DB.get_user(username)
    if isinstance(user, dict):
        challenge = uuid.uuid4().hex
        return jsonify({"salt": user['salt'], "challenge": challenge})
    else:
        return "no user found"

@APP.route("/signin2", methods=['POST'])
def second_signin():
    '''second sign in, return JWT token'''
    content = request.get_json(force=True)
    username = (content['username']).encode('ascii', 'ignore')
    tag = (content['tag']).encode('ascii', 'ignore')
    challenge = (content['challenge']).encode('ascii', 'ignore')
    user = DB.get_user(username)
    new_tag = hmac.new(user['hashed_pwd'], challenge, hashlib.sha512)
    if hmac.compare_digest(tag, new_tag.hexdigest()):
        return jwt.encode({'username': username, 'exp': int(time.time())+3600}, 'mysecret', algorithm='HS512')
    else:
        abort(403)

@APP.route("/get_message", methods=['GET'])
def get_message():
    '''return message back to user'''
    jwt_token = request.headers.get('Auth')
    result = jwt.decode(jwt_token, 'mysecret')
    return result['username']
    #need to implement this method

@APP.route("/send_message", methods=['POST'])
def send_message():
    '''accept message from user'''
    #based on JWT token, get username and information, and insert to database
    content = request.get_json(force=True)
    frmUsr = content['from']
    toUsr = content['to']
    msg = content['msg']
    time = content['time']
    isRead = 0
    # perform insert here
    return "Message"

if __name__ == '__main__':
    APP.run(host='0.0.0.0')

