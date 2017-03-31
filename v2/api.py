#!/usr/bin/env python
'''api for secured chat application'''
import hmac
import hashlib
import uuid
import binascii
import logging
from flask import Flask, request, jsonify, abort
import scrypt

LOGGER = logging.getLogger("api")
LOGGER.setLevel(logging.INFO)
HANDLER = logging.FileHandler('/var/log/seenada/api.log')
HANDLER.setLevel(logging.INFO)
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

APP = Flask(__name__)

@APP.route("/")
def hello():
    '''basic homepage for testing'''
    return "Hello. Welcome"

@APP.route("/register", methods=['POST'])
def register():
    '''new user sign up'''
    content = request.get_json(force=True)
    username = content['username']
    pwd = (content['password']).encode('ascii', 'ignore')
    salt = uuid.uuid4().hex
    hashed_binary_pwd = scrypt.hash(pwd, salt)
    hashed_pwd = binascii.hexlify(hashed_binary_pwd)
    LOGGER.info(hashed_pwd)
    return jsonify({"username": username, "password": hashed_pwd, "salt": salt})
    #need to:
    #insert username into username table and get id out
    #insert id, salt, hashed password into pwd table

@APP.route("/signin1", methods=['POST'])
def first_signin():
    '''first signin, return salt'''
    content = request.get_json(force=True)
    username = content['username']
    #what need to be done:
    #query userid and then result salt with challenge c
    return True

@APP.route("/signin2", methods=['POST'])
def second_signin():
    '''second sign in, return JWT token'''
    content = request.get_json(force=True)
    username = content['username']
    tag = content['tag']
    challenge = content['challenge']
    #what need to be done
    #based on username, get userid and query hashed_password
    #key = hashed_password
    new_tag = hmac.new('sharedkey', challenge, hashlib.sha512)
    if hmac.compare_digest(tag, new_tag):
        return True

@APP.route("/get_message", methods=['GET'])
def get_message():
    '''return message back to user'''
    #based on JWT token, get username, and query unread message from database
    return "Message"

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

