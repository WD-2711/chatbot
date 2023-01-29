#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/14 17:44:10
# @Author: wd-2711
'''

from .config.config import *

config = getConfig()
ST_token = config['st_token']
ED_token = config['ed_token']
data_path = config['processor_result']
samples_num = config['samples_num']

class DataRecorder:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "ST", 1: "ED"}
        self.n_word = 2
    
    def addSentence(self, sentence):
        for word in sentence.split(" "):
            self.__addWord(word)
    
    def __addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_word
            self.word2count[word] = 1
            self.index2word[self.n_word] = word
            self.n_word += 1
        else:
            self.word2count[word] += 1

def tensor_from_sentence(recorder, sentence):
    indexes = [recorder.word2index[w] for w in sentence.split(' ')]
    indexes.append(ED_token)
    return torch.tensor(indexes, dtype = torch.long, device = device).view(-1, 1)

class DataLoader():
    def __init__(self):

        self.data = []
        self.inp_recorder = DataRecorder("ask")
        self.out_recorder = DataRecorder("resp")


    def __create_dataset(self):
        with open(data_path, 'r', encoding = 'utf-8') as f:
            self.data = f.readlines()[:samples_num]
            self.data = [['ST ' + dd + ' ED' for dd in d.replace('\n', '').strip().split('\t')] for d in self.data]
            self.inp_recorder = DataRecorder("ask")
            self.out_recorder = DataRecorder("resp")
            for d in self.data:
                self.inp_recorder.addSentence(d[0])
                self.out_recorder.addSentence(d[1])
                
    def run(self):
        inp_tensors = []
        targ_tensors = []
        self.__create_dataset()
        for i in range(0, samples_num - 1):
            inp_tensor = tensor_from_sentence(self.inp_recorder, self.data[i][0])
            targ_tensor = tensor_from_sentence(self.out_recorder, self.data[i][1])
            inp_tensors.append(inp_tensor)
            targ_tensors.append(targ_tensor)
        return inp_tensors, self.inp_recorder, targ_tensors, self.out_recorder

if __name__ == "__main__":
    model = DataLoader()
    print(model.run())