#!/usr/bin/env python
'''a class to access database'''
import logging
import pymysql

LOGGER = logging.getLogger("DbAccess")
LOGGER.setLevel(logging.INFO)
HANDLER = logging.FileHandler('/var/log/seenada/DbAccess.log')
HANDLER.setLevel(logging.INFO)
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

class DbAccess(object):
    '''class to access db'''
    def __init__(self):
        '''init value'''
        self.__conn = None
        self.__cursor = None

    def get_connection(self):
        '''create db connection'''
        try:
            self.__conn = pymysql.connect(host='localhost',\
                                            port=3306,\
                                            user='python',\
                                            passwd='123456',\
                                            db='seenada_v1')
            self.__cursor = self.__conn.cursor()
            return 'ok'
        except Exception as error:
            LOGGER.exception(error)
            return 'error'

    def add_user(self, username, salt, hashed_pwd):
        '''add user into database'''
        return True

    def get_user(self, username):
        '''get user from username'''
        return True

    def add_message(self, message_obj):
        '''add message into database'''
        return True

    def get_unread_message(self, username):
        '''get unread message for a user'''
        return True
