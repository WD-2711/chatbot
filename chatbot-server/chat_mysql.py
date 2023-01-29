#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/28 15:39:50
# @Author: wd-2711
# @Destription:
    This code is modified based on https://github.com/stormzhuo0707/pythonProject/blob/main/python_chat/chat_mysql.py.
    Aims to check username and passwd, and save data.
'''

import pymysql

class LogInformation(object):
    @staticmethod
    def connect_db():
        db = pymysql.connect(
            host = "127.0.0.1", 
            user = "root", 
            password = "root", 
            db = "chatbot_info"
        )
        cursor = db.cursor()   
        return db, cursor     
    
    @staticmethod
    def login_check(user_name, password):
        db, cursor = LogInformation.connect_db()
        sql = "SELECT * FROM user_info where user_name = '%s' " % (user_name)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            db.close() 
            return password == results[1]
        except Exception as e:
            print("[+] login_check error: ", e)
            db.close()
            return False

    @staticmethod
    def create_new_user(user_name, password, file_name):
        db, cursor = LogInformation.connect_db()
        sql = "INSERT INTO user_info VALUES ('%s','%s','%s');" % (user_name, password, file_name)
        try:
            cursor.execute(sql) 
            db.commit()
            db.close()
            return True
        except Exception as e:
            print("[+] create_new_user error: ", e)
            db.rollback() 
            db.close() 
            return False

    @staticmethod
    def select_user_name(user_name):
        db, cursor = LogInformation.connect_db()
        sql = "SELECT * FROM user_info where user_name = '%s' " % (user_name)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            db.close()
            return True if results != None else False
        except Exception as e:
            print("[+] select_user_name error: ", e)
            db.close()
            return False










