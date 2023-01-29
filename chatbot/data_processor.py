#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/14 17:16:01
# @Author: wd-2711
'''

from config.config import *

config = getConfig()
data_path = config['source_data']
end_flag = config['end_flag']
con_flag = config['con_flag']
result_path = config['processor_result']

def sentenceCutter(sentence):
    sentence = sentence.strip('\n')
    sentence = re.sub(r"[%s]+" % punctuation, " ", sentence)
    if sentence == "": return sentence
    return " ".join(jieba.cut(sentence))

def dataProcessor():
    print(data_path)
    if not os.path.exists(data_path):
        print("[+] source data not exist!")
        exit()
    if os.path.exists(result_path):
        print("[+] data_processor.py have runned before.")
        return

    convs = []
    with open(data_path, 'r', encoding = 'utf-8') as f:
        one_conv = []
        for line in f:
            line = line.strip('\n')
            line = re.sub(r"[%s]+" % punctuation, " ", line)
            if line == "": continue
            if line[0] == end_flag:
                if one_conv:
                    convs.append(one_conv)
                one_conv = []
            elif line[0] == con_flag:
                one_conv.append(line.split(" ")[1])

    seq = []
    for conv in convs:
        conv.remove("") if "" in conv else conv
        if len(conv) == 1: continue
        if len(conv) % 2 != 0: conv = conv[:-1]
        for i in range(len(conv)):
            if i % 2 == 0:
                conv[i] = " ".join(jieba.cut(conv[i]))
                conv[i + 1] = " ".join(jieba.cut(conv[i + 1]))
                seq.append(conv[i] + '\t' + conv[i + 1])
    print("[+] data participle have done.")

    with open(result_path, 'w', encoding = 'utf-8') as f:
        for i in tqdm(range(len(seq))):
            f.write(seq[i] + '\n')
    print("[+] data result have write into {}.".format(result_path))

if __name__ == "__main__":
    dataProcessor()