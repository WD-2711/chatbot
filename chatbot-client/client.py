
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/29 12:44:04
# @Author: wd-2711
# @Destription:
    Client.py used to connect with server.
    It define three send func (login, register_user, send_message).
'''

import math
import socket

class ChatSocket:
    def __init__(self):
        print("[+] Init tcp client")
        self.client_socket = socket.socket()
        self.client_socket.connect(('your server ip', 7777))

    def login(self, user_name, password):
        self.client_socket.sendall(bytes("1", "utf-8"))
        self.send_string_with_length(user_name)
        self.send_string_with_length(password)
        check_result = self.recv_string_by_length(1) 
        return check_result 

    def register_user(self, user_name, password, file_name):
        self.client_socket.sendall(bytes("2", "utf-8"))
        self.send_string_with_length(user_name)
        self.send_string_with_length(password)
        self.send_string_with_length(file_name)
        return self.recv_string_by_length(1)

    def send_message(self, message):
        self.client_socket.sendall(bytes("3", "utf-8"))
        self.send_string_with_length(message)

    """
    send msg
    """
    def send_string_with_length(self, content):
        self.client_socket.sendall(bytes(content, encoding = 'utf-8').__len__().to_bytes(4, byteorder = 'big'))
        self.client_socket.sendall(bytes(content, encoding = 'utf-8'))

    """
    recev msg by length
    """
    def recv_string_by_length(self, len):
        return str(self.client_socket.recv(len), "utf-8")

    def recv_all_string(self):
        length = int.from_bytes(self.client_socket.recv(4), byteorder = 'big') 
        b_size = 3 * 1024
        times = math.ceil(length / b_size)
        content = ''
        for i in range(times):
            if i == times - 1:
                seg_b = self.client_socket.recv(length % b_size)
            else:
                seg_b = self.client_socket.recv(b_size)
            content += str(seg_b, encoding = 'utf-8')
        return content

