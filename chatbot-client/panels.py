#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/23 18:18:07
# @Author: wd-2711
# @Destription:
    Panels.py include many panels (register, login, main).
    These define panels looks like.
'''

import time
from tkinter import *
from PIL import ImageTk, Image
import tkinter.font as tf

class Panel(object):
    def __init__(self):
        return

    def init_setter(self, tk_obj, w, h, title):

        # width and height
        screen_width = tk_obj.winfo_screenwidth()
        screen_height = tk_obj.winfo_screenheight()
        gm_str = "%dx%d+%d+%d" % (
            w, 
            h, 
            (screen_width - w) / 2,
            (screen_height - 1.2 * h) / 2
        )
        tk_obj.geometry(gm_str)
        tk_obj.title(title)
        tk_obj.resizable(width = False, height = False) 

    def background_setter(self, tk_obj, filename):
        self.bg = ImageTk.PhotoImage(file = filename)
        img_label = Label(
            tk_obj
        )
        img_label.place(
            relx = 0.0, 
            rely = 0.0, 
            relwidth = 1, 
            relheigh = 1
        )
        img_label.configure(image = self.bg)   

class RegisterPanel(Panel):
    def __init__(self, file_open_face, close_register_window, register_submit):
        super().__init__()
        self.file_open_face = file_open_face
        self.close_register_window = close_register_window
        self.register_submit = register_submit
        self.file_name = ""
    
    def show_register_panel(self):

        self.register_frame = Tk()

        # width and height
        self.init_setter(self.register_frame, 503, 400, "Register")

        # register background
        self.background_setter(self.register_frame, 'images/register_bg.jpg')

        # name + passwd + confirm passwd
        Label(
            self.register_frame, 
            text = 'Name   ', 
            font = ('Times New Roman', 12), 
        ).place(x = 75, y = 230)
        Label(
            self.register_frame, 
            text = 'Passwd ', 
            font = ('Times New Roman', 12), 
        ).place(x = 75, y = 260) 
        Label(
            self.register_frame, 
            text = 'Confirm', 
            font = ('Times New Roman', 12), 
        ).place(x = 75, y = 290)          
        self.user_name = StringVar()
        self.passwd = StringVar()
        self.confirm_passwd = StringVar()
        Entry(
            self.register_frame, 
            textvariable = self.user_name,
            width = 30,        
        ).place(x = 140, y = 230)
        Entry(
            self.register_frame, 
            textvariable = self.passwd,
            width = 30,
            show = '*',            
        ).place(x = 140, y = 260)
        Entry(
            self.register_frame, 
            textvariable = self.confirm_passwd,
            width = 30,
            show = '*',         
        ).place(x = 140, y = 290)

        # button
        Button(
            self.register_frame,
            bg = 'gray',
            fg = 'white',
            text = 'Return',
            font = ('Times New Roman', 15),
            command = self.close_register_window,
            width = 8
        ).place(x = 130, y = 330)
        Button(
            self.register_frame,
            text = 'Register',
            bg = 'gray',
            fg = 'white',
            width = 8,
            font = ('Times New Roman', 15),
            command = lambda:self.register_submit(self)    
        ).place(x = 250, y = 330)        
        default_head_path = "images/set_head_img.png"
        Image.open(default_head_path).resize(
            (70, 70), 
            Image.ANTIALIAS
        ).save(default_head_path, "png")
        self.head_img = PhotoImage(file = default_head_path)
        self.face_show = Button(
            self.register_frame,
            image = self.head_img,
            bd = 5,
            command = lambda:self.file_open_face(self)    
        )
        self.face_show.place(x = 210, y = 130)  

    def load(self):
        self.register_frame.mainloop()

    def add_face(self, file_name):
        self.file_name = file_name
        head_path = "images/head_image.png"
        Image.open(self.file_name).resize(
            (70, 70), 
            Image.ANTIALIAS
        ).save(head_path, "png")
        self.p = PhotoImage(file = head_path)
        self.face_show.config(image = self.p)
   

    def close_register_panel(self):
        if self.register_frame == None:
            print("[+] close_register_panel error.")
        else:
            self.register_frame.destroy()
    
    def get_input(self):
        return self.user_name.get(), self.passwd.get(), self.confirm_passwd.get(), self.file_name

class LoginPanel(Panel):
    def __init__(self, handle_login, handle_register, close_login_window):
        super().__init__()
        self.handle_login = handle_login
        self.handle_register = handle_register
        self.close_login_window = close_login_window
    
    def show_login_panel(self):    
        self.login_frame = Tk()

        # height and width
        self.login_frame.protocol("WM_DELETE_WINDOW", self.close_login_window)
        self.init_setter(self.login_frame, 503, 400, "Login")

        # login background
        self.background_setter(self.login_frame, 'images/login_bg.jpg')

        # name and passwd
        Label(
            self.login_frame, 
            text = 'Name  ', 
            font = ('Times New Roman', 12), 
            fg = 'black'
        ).place(x = 115, y = 230)
        Label(
            self.login_frame, 
            text = 'Passwd', 
            font = ('Times New Roman', 12), 
            fg = 'black'
        ).place(x = 115, y = 260) 
        self.user_name = StringVar()
        self.passwd = StringVar() 
        Entry(
            self.login_frame,
            textvariable = self.user_name,
            fg = 'black',
            width = 25
        ).place(x = 180, y = 230)
        Entry(
            self.login_frame,
            textvariable = self.passwd,
            show = '*',
            fg = 'black',
            width = 25            
        ).place(x = 180, y = 260)

        # register button   
        Button(
            self.login_frame,
            text = 'register',
            bg = 'gray',
            fg = 'white',
            font = ('Times New Roman', 15),
            command = self.handle_register,
            width = 6
        ).place(x = 150, y = 300)

        # login button
        Button(
            self.login_frame,
            text = 'login',
            bg = 'gray',
            fg = 'white',
            font = ('Times New Roman', 15),
            command = lambda:self.handle_login(self),
            width = 6
        ).place(x = 270, y = 300)

    def load(self):
        self.login_frame.mainloop()
    
    def close_login_panel(self):
        if self.login_frame == None:
            print("[+] close_login_panel error.")
        else:
            self.login_frame.destroy()
    
    def get_input(self):
        return self.user_name.get(), self.passwd.get()

class MainPanel(Panel):
    def __init__(self, user_name, send_message, close_main_window):
        super().__init__()
        self.user_name = user_name
        self.send_message = send_message
        self.close_main_window = close_main_window

        Image.open("images/chatbot_img.png").resize(
            (50, 50), 
            Image.ANTIALIAS
        ).save("images/chatbot_img_mp.png", 'png')
        Image.open("images/head_image.png").resize(
            (50, 50), 
            Image.ANTIALIAS
        ).save("images/head_image_mp.png", "png")
        self.faces = []
        
    def show_main_panel(self):

        self.main_frame = Tk()
        self.main_frame.protocol("WM_DELETE_WINDOW", self.close_main_window)
        self.init_setter(self.main_frame, 650, 700, "ChatBot")

        # background
        self.background_setter(self.main_frame, 'images/main_bg.jpg')

        # message box
        msg_sc_bar = Scrollbar(self.main_frame) 
        msg_sc_bar.grid(
            row = 0, 
            column = 1, 
            sticky = E + N + S, 
            pady = (30, 0)
        )
        self.message_text = Text(
            self.main_frame, 
            bg = "white", 
            height = 40,
            highlightcolor = "white", 
            highlightthickness = 1,
        )
        self.message_text.config(state = DISABLED)
        self.message_text.grid(
            row = 0, 
            column = 0, 
            sticky = W + E + N + S, 
            padx = (30, 0),
            pady = (30, 0)
        )
        msg_sc_bar["command"] = self.message_text.yview
        self.message_text["yscrollcommand"] = msg_sc_bar.set

        # input box
        send_sc_bar = Scrollbar(self.main_frame)
        send_sc_bar.grid(
            row = 1, 
            column = 1, 
            sticky = E + N + S,  
            pady = (20, 0)
        )

        # input box
        self.send_text = Text(
            self.main_frame, 
            bg = "white", 
            height = 5, 
            highlightcolor = "white",
            highlightbackground = "#444444", 
            highlightthickness = 0
        )
        self.send_text.see(END)
        self.send_text.grid(
            row = 1, 
            column = 0, 
            sticky = W + E + N + S, 
            padx = (30, 0),
            pady = (20, 0)
        )
        send_sc_bar["command"] = self.send_text.yview
        self.send_text["yscrollcommand"] = send_sc_bar.set

        # send button
        Button(
            self.main_frame, 
            command = lambda: self.send_message(self), 
            text = "Send", 
            bg = "gray",
            fg = "white", 
            width = 20, 
            height = 1, 
            font = ('Times New Roman', 12)
        ).place(x = 235, y = 655)

    def load(self):
        self.main_frame.mainloop()

    def show_send_message(self, user_name, content):
        if user_name == "bot":
            face_path = "images/chatbot_img_mp.png",
        else:
            face_path = "images/head_image_mp.png",          
        time.sleep(0.5)

        self.message_text.config(state = NORMAL)
        ft = tf.Font(family = 'Times New Roman', size = 13)
        self.message_text.tag_config("tag_7", foreground = "black", font = ft)
        title = "\n" + user_name + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
        self.message_text.insert(END, title, 'tag_7')

        time.sleep(0.5)
        self.faces.append(PhotoImage(file = face_path))
        self.message_text.image_create(END, image = self.faces[-1])
        self.message_text.insert(END, " : ")
        ft = tf.Font(family = 'Times New Roman', size = 15)
        self.message_text.tag_config("tag_8", foreground = "black", font = ft)
        self.message_text.insert(END, content, 'tag_8')

        self.message_text.config(state = DISABLED)
        self.message_text.see(END)


    def clear_send_text(self):
        self.send_text.delete('0.0', END)

    def get_send_text(self):
        return self.send_text.get('0.0', END)