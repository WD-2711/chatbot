#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/29 12:41:52
# @Author: wd-2711
# @Destription:
    Main.py define some handler function to process window close, submit and so on.
'''

import os
from tkinter import messagebox
import threading
import time
import tkinter.filedialog
import panels
import client

def close_login_window():
    client.client_socket.close()
    login_module.login_frame.destroy()

def close_main_window():
    client.client_socket.close()
    main_module.main_frame.destroy() 

def file_open_face(self):
    file_name = tkinter.filedialog.askopenfilename()
    if file_name != '':
        self.add_face(file_name)
    else:
        messagebox.showwarning("Notice", "you havn't choose any file!")
        return

def handding_login(self):
    user_name, password = self.get_input()
    if user_name == "":
        messagebox.showwarning("Notice", "username is empty!")
        return
    if password == "":
        messagebox.showwarning("Notice", "password is empty!")
        return
    if client.login(user_name, password) == "1":
        go_to_main_panel(user_name)
    else:
        messagebox.showwarning("Notice", "username or password is wrong!")
        return

def handding_register():
    global register_module
    login_module.close_login_panel()
    register_module = panels.RegisterPanel(file_open_face, close_register_window, register_submit)
    register_module.show_register_panel()
    register_module.load()

def close_register_window():
    global login_module
    register_module.close_register_panel()
    login_module = panels.LoginPanel(handding_login, handding_register, close_login_window)
    login_module.show_login_panel()
    login_module.load()

def register_submit(self):
    user_name, password, confirm_password, file_name = self.get_input()

    if user_name == "" or password == "" or confirm_password == "":
        messagebox.showwarning("wrong", "please fill this form")
        return
    if len(password) < 8:
        messagebox.showwarning("wrong", "your password short just like your dick(<8cm)")
        return        
    if not password == confirm_password:
        messagebox.showwarning("wrong", "two passwords not same")
        return
    if self.file_name == "":
        messagebox.showwarning("wrong", "please choose head image")
        return

    result = client.register_user(user_name, password, file_name)

    if result == "0":
        messagebox.showerror("wrong", "this name has been registered")
        return
    elif result == "1":
        messagebox.showinfo("success", "register success!")
        return
        close_register_window()        
    elif result == "2":
        messagebox.showerror("wrong", "unknown mistake")
        return

def send_message(self):
    content = main_module.get_send_text()
    if content == "" or content == "\n":
        messagebox.showwarning("Notice", "empty msg")
        return
    main_module.clear_send_text()
    client.send_message(content)
    main_module.show_send_message(main_module.user_name, content)

def go_to_main_panel(user_name):
    global main_module
    login_module.close_login_panel()
    main_module = panels.MainPanel(user_name, send_message, close_main_window)

    threading.Thread(target = recv_data).start()
    main_module.show_main_panel() 
    main_module.load() 

def recv_data():
    time.sleep(1)
    while True:
        try:
            data_type = client.recv_all_string()
            if data_type == "#!resp#!":
                user = client.recv_all_string()
                content = client.recv_all_string()
                main_module.show_send_message(user, content)
        except Exception as e:
            print("[+] error:", str(e))
            break

def go_to_login_panel():
    global client, login_module
    client = client.ChatSocket()
    login_module = panels.LoginPanel(handding_login, handding_register, close_login_window)
    login_module.show_login_panel()
    login_module.load()


if __name__ == "__main__":
    go_to_login_panel()
