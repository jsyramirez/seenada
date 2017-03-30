#!/usr/bin/env python
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
    return jsonify({"username": username, "password": hashed_pwd})
    #need to:
    #insert username into username table and get id out
    #insert id, salt, hashed password into pwd table
if __name__ == '__main__':
    APP.run(host='0.0.0.0')

