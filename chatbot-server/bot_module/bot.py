#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/14 17:41:46
# @Author: wd-2711
# @Destription:
    Chatbot module, see chatbod dir for details.
    Use 75 epoch model.
'''

from .trainer import chatbot

model = chatbot()
def bot(inp):
    model_file = "./bot_module/models/seq2seqModel_75.pt"
    resp = model.predict(inp, model_file)
    return resp if resp == "input error" else resp.replace(' ', '')[2:-7]

