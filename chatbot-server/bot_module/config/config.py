#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/16 14:09:28
# @Author: wd-2711
'''

# dependent library
import os
import re
import jieba
import sys
import time
from tqdm import tqdm
from zhon.hanzi import punctuation
from configparser import SafeConfigParser
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim

# device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("[+] using device [{}]".format(device))

# config
config_file = './bot_module/config/config.ini'
def getConfig():
    if not os.path.exists(config_file):
        print("[+] config file not exist.")
        exit()
    parser = SafeConfigParser()
    parser.read(config_file, encoding = 'utf-8')
    ints = [(k, int(v)) for k, v in parser.items('ints')]
    floats = [(k, float(v)) for k, v in parser.items('floats')]
    strings = [(k, str(v)) for k, v in parser.items('strings')]
    return dict(ints + floats + strings)


