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
    try:
        username = (content['username']).encode('ascii', 'ignore')
        tag = (content['tag']).encode('ascii', 'ignore')
        challenge = (content['challenge']).encode('ascii', 'ignore')
        user = DB.get_user(username)
        new_tag = hmac.new(user['hashed_pwd'], challenge, hashlib.sha512)
        if hmac.compare_digest(tag, new_tag.hexdigest()):
            return jwt.encode({'username': username,
                               'exp': int(time.time())+3600},
                              'mysecret', algorithm='HS512')
        else:
            LOGGER.debug('Tag does not match')
            abort(403)
    except KeyError as err:
        LOGGER.error('Invalid JSON')
        LOGGER.exception(err)
        abort(403)

@APP.route("/get_message", methods=['GET'])
def get_message():
    '''return message back to user'''
    jwt_token = request.headers.get('Auth', None)
    if jwt_token is not None:
        result = jwt.decode(jwt_token, 'mysecret')
        this_moment = int(time.time())
        token_exp = result.get('exp', None)
        print token_exp
        print this_moment
        username = result.get('username', '')
        if (token_exp is not None) and (this_moment <= token_exp):
            return jsonify(DB.get_unread_message(username))
        else:
            LOGGER.debug(token_exp)
            return jsonify({'Error': 'Token has expired. Please re-sigin'})
    else:
        abort(403)

@APP.route("/send_message", methods=['POST'])
def send_message():
    '''accept message from user'''
    #based on JWT token, get username and information, and insert to database
    jwt_token = request.headers.get('Auth', None)
    if jwt_token is not None:
        content = request.get_json(force=True)
        response = DB.add_message(content)
        if response == 'ok':
            return "Success"
        else:
            return "Error"
    else:
        abort(403)

if __name__ == '__main__':
    APP.run(host='0.0.0.0')

