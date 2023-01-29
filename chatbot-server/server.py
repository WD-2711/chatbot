#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/29 12:55:39
# @Author: wd-2711
# @Destription:
    Server.py should be placed on the server.
    Connect with client.
'''

import socket 
from threading import Thread 
import math
import chat_mysql 
from bot_module.bot import *

def send_string_with_length(_conn, content):
    _conn.sendall(bytes(content, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))
    _conn.sendall(bytes(content, encoding='utf-8'))

def send_number(_conn, number):
    _conn.sendall(int(number).to_bytes(4, byteorder='big'))

def recv_all_string(connection):
    length = int.from_bytes(connection.recv(4), byteorder='big')
    b_size = 3 * 1024  
    times = math.ceil(length / b_size)
    content = ''
    for i in range(times):
        if i == times - 1:
            seg_b = connection.recv(length % b_size)
        else:
            seg_b = connection.recv(b_size)
        content += str(seg_b, encoding='utf-8')
    return content

def check_user(user_name, password):
    return chat_mysql.LogInformation.login_check(user_name, password)

def add_user(user_name, password, file_name):
    """
        USER EXIST   --> 0
        USER SATISFY --> 1
        ERROR        --> 2
    """
    if chat_mysql.LogInformation.select_user_name(user_name):
        return "0"
    elif chat_mysql.LogInformation.create_new_user(user_name, password, file_name):
        return "1"
    else:
        return "2"

def handle_login(connection, address):
    user_name = recv_all_string(connection)
    password = recv_all_string(connection)
    check_result = check_user(user_name, password)
    if check_result:
        connection.sendall(bytes("1", "utf-8"))
    else:
        connection.sendall(bytes("0", "utf-8"))
    return True


def handle_register(connection, address):
    user_name = recv_all_string(connection)
    password = recv_all_string(connection)
    file_name = recv_all_string(connection)
    connection.sendall(bytes(add_user(user_name, password, file_name), "utf-8"))
    return True

def handle_message(connection, address):
    content = recv_all_string(connection).replace("\n", "")
    send_string_with_length(connection, "#!resp#!")
    send_string_with_length(connection, "bot")
    resp = bot(content)
    send_string_with_length(connection, resp)
    print("[+] chat:", content, resp)
    return True

def handle(connection, address):
    try:
        while True:
            request_type = str(connection.recv(1024).decode())
            no_go = True
            if request_type == "1":
                print("[+] handling login request")
                no_go = handle_login(connection, address)
            elif request_type == "2":
                print("[+] handling register request")
                no_go = handle_register(connection, address)
            elif request_type == "3":
                print("[+] handling message request")
                no_go = handle_message(connection, address)
            if not no_go:
                break
    except Exception as e:
        print("[+] error:", str(e))
    finally:
        try:
            connection.close()
        except Exception as e:
            print("[+] error:", str(e))

if __name__ == "__main__":
    try:
        server = socket.socket()
        server.bind(('0.0.0.0', 7777))
        server.listen(10)
        print("[+] begin listening")
        while True:
            connection, address = server.accept()
            Thread(
                target = handle, 
                args = (connection, address)
            ).start()
    except Exception as e:
        print("[+] error:", str(e))
