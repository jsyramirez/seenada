#!/usr/bin/env python
import logging
import pymysql

logging.basicConfig(filename='/var/log/DbAccess.log', level=logging.DEBUG, format='%(asctime)-15s  %(user)-8s %(message)s')
logger = logging.getLogger('DbAccess')
class DbAccess:
    '''DB class to connect to database'''
    def __init__(self):
        '''Init the variable and get connection'''
        self.__conn = None
        self.__cursor = None
        self.get_connection()

    def get_connection(self):
        '''get connection and assign to __conn and __cursor'''
        try:
            self.__conn = pymysql.connect(host='localhost', port=3306, user='python', passwd='123456', db='seenada_v1')
            self.__cursor = self.__conn.cursor()
            return self.__cursor
        except Exception as error:
            logger.error(error)

    def insert_user(self, username, password):
        '''insert user into database'''
        try:
            self.__cursor.execute("insert into user values (%s, %s)", (username, password))
            self.__conn.commit()
        except Exception as error:
            logger.error(error)
    def get_all_user(self):
        self.__cursor.execute("select * from user")
        result = self.__cursor.fetchall()
        print result
    def get_user(self, username):
        self.__cursor.execute("select * from user where username = %s", (username,))
        return self.__cursor.fetchone()
