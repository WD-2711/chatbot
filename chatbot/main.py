#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/14 17:41:46
# @Author: wd-2711
'''

from trainer import chatbot

if __name__ == "__main__":
    # train mode
    """
    model = chatbot()
    model.trainer()
    print(model.predict('你好啊！'))   
    """

    # test mode
    model = chatbot()
    model_file = "./models/seq2seqModel_75.pt"
    while True:
        inp = input("please input your ask:")
        if inp == "":
            break
        print(inp, model.predict(inp, model_file))

