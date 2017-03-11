#!/usr/bin/env python
'''class to access and query database'''
import logging
import pymysql

logging.basicConfig(filename='/var/log/DbAccess.log', level=logging.DEBUG, format='%(asctime)-15s  %(user)-8s %(message)s')
logger = logging.getLogger('DbAccess')
class DbAccess(object):
    '''DB class to connect to database'''
    def __init__(self):
        '''Init the variable and get connection'''
        self.__conn = None
        self.__cursor = None
        #self.get_connection()

    def get_connection(self):
        '''get connection and assign to __conn and __cursor'''
        try:
            self.__conn = pymysql.connect(host='localhost',\
                                            port=3306,\
                                            user='python',\
                                            passwd='123456',\
                                            db='seenada_v1')
            self.__cursor = self.__conn.cursor()
            return self.__cursor
        except Exception as error:
            logger.error(error)

    def insert_user(self, username, password):
        '''insert user into database'''
        try:
            self.get_connection()
            self.__cursor.execute("insert into user values (%s, %s)",\
                                    (username, password))
            self.__conn.commit()
            self.__conn.close()
            return 'success'
        except Exception as error:
            logger.error(error)
    def get_all_user(self):
        '''get all user'''
        self.get_connection()
        self.__cursor.execute("select * from user")
        result = self.__cursor.fetchall()
        self.__conn.close()
        return result

    def get_user(self, username):
        '''get a user'''
        self.get_connection()
        self.__cursor.execute("select * from user where username = %s",\
                                (username,))
        self.__conn.close()
        return self.__cursor.fetchone()

    def insert_message(self, message):
        '''insert a message'''
        self.get_connection()
        try:
            frmUser = message['from']
            toUser = message['to']
            content = message['content']
            timestamp = message['timestamp']
            values = (frmUser, toUser, content, 0, timestamp)
            self.__cursor.execute("insert into messages(from_user, to_user, content, isRead, timestamp)\
                                    values(%s, %s, %s, %s, %s)", values)
            self.__conn.commit()
            self.__conn.close()
            return 'success'
        except KeyError as error:
            return "Error: {}. Please check the db definition for a list of column".format(str(error))
        except pymysql.MySQLError as err:
            return "Error: {}. Please check db if there is any issue".format(str(err))

    def get_message(self, user):
        '''get unread message for an user'''
        self.get_connection()
        self.__cursor.execute('select * from messages where to_user=%s and isRead=0', (user,))
        results = self.__cursor.fetchall()
        for result in results:
            self.__cursor.execute('update messages set isRead=1 where id=%s', (result[0],))
        self.__conn.commit()
        self.__conn.close()
        return results
