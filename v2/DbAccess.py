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
                                            db='seenada_v2')
            self.__cursor = self.__conn.cursor()
            return 'ok'
        except pymysql.Error as error:
            LOGGER.exception(error)
            return 'error'

    def close_connection(self):
        '''close connection'''
        if self.__conn.open:
            self.__conn.close()

    def add_user(self, username, salt, hashed_pwd):
        '''add user into database'''
        if self.get_connection() == 'ok':
            try:
                self.__cursor.execute("insert into users(username) value (%s)", (username,))
                self.__cursor.execute("select * from users where username = %s", (username,))
                result = self.__cursor.fetchone()
                if result is not None:
                    values = (result[0], salt, hashed_pwd)
                    self.__cursor.execute("insert into pwd values (%s, %s, %s)", values)
                    self.__conn.commit()
                    return 'ok'
                else:
                    LOGGER.error('Insert failed')
                    return 'error'
            except pymysql.Error as error:
                LOGGER.exception(error)
                return 'error'
            finally:
                self.close_connection()
        else:
            return 'no connection'

    def get_user(self, username):
        '''get user from username'''
        if self.get_connection() == 'ok':
            try:
                self.__cursor.execute("select users.id, users.username, pwd.salt, pwd.password\
                                       from users inner join pwd on users.id = pwd.id\
                                       where username = %s", (username,))
                result = self.__cursor.fetchone()
                if result is not None:
                    return {'id': result[0], 'username': result[1],
                            'salt': result[2], 'hashed_pwd': result[3]}
                else:
                    LOGGER.debug('No result from query')
                    return {}
            except pymysql.Error as err:
                LOGGER.exception(err)
                return 'error'
            finally:
                self.close_connection()
        else:
            return 'no connection'

    def add_message(self, message_obj):
        '''add message into database'''
        if self.get_connection() == 'ok':
            try:
                values = (message_obj['from'], message_obj['to'],
                          message_obj['message'], message_obj['time'], 1)
                self.__cursor.execute("insert into messages\
                                      (fromUsr, toUsr, content, timestamp, isRead)\
                                      values (%s, %s, %s, %s, %s)", values)
                self.__conn.commit()
                return 'ok'
            except pymysql.Error as err:
                LOGGER.exception(err)
                return 'error'
            finally:
                self.close_connection()
        else:
            return 'no connection'

    def get_unread_message(self, username):
        '''get unread message for a user'''
        if self.get_connection() == 'ok':
            try:
                self.__cursor.execute("select * from messages\
                                       where username = %s and isRead = 0", (username,))
                result = self.__cursor.fetchall()
                if result is None:
                    return 'No new message'
                else:
                    return {"from": result[1], "to": result[2],
                            "message": result[3], "timestamp": result[4]}
            except pymysql.Error as err:
                LOGGER.exception(err)
                return 'error'
            finally:
                self.close_connection()
        else:
            return 'no connection'
