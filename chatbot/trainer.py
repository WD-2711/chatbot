#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/14 17:42:23
# @Author: wd-2711
'''

from data_processor import sentenceCutter, dataProcessor
from data_loader import DataLoader, tensor_from_sentence
from models.seq2seq_model import Encoder, AttentionDecoder, train_step
from config.config import *

config = getConfig()
MAX = 100000

class chatbot:
    def __load_data(self):
        st = time.time()
        dataProcessor()
        self.inp_tensors, self.inp_recorder, self.targ_tensors, self.out_recorder = DataLoader().run()
        print("[+] loaded train data cost {:.2f}s".format(time.time() - st))        

    def __init__(self):
        self.hidden_size = config['hidden_size']
        self.batch_size = config['batch_size']
        self.model_file = config['model_file']
        self.gate_loss = config['gate_loss']
        self.samples_num = config['samples_num']
        self.max_length = config['max_length']
        self.device = device
        self.ST_token = config['st_token']
        self.ED_token = config['ed_token']
  
        self.inp_recorder, self.out_recorder = None, None
        self.__load_data()

    def trainer(self):
        encoder = Encoder(self.inp_recorder.n_word, self.hidden_size).to(device)
        decoder = AttentionDecoder(self.hidden_size, self.out_recorder.n_word, dropout_p = 0.1).to(device)

        if os.path.exists(self.model_file):
            print("[+] model has been trained before. Loading {}.".format(self.model_file))
            check_point = torch.load(self.model_file)
            encoder.load_state_dict(check_point['encoder_dict'])
            decoder.load_state_dict(check_point['decoder_dict'])

        print("[+] begin training...")
        total_loss = 0
        batch_loss = 0
        epoch_loss = MAX
        epoch_ind = 0
        steps_num = range(1, self.samples_num // self.batch_size)
        print("[+] steps per epoch: {}".format(len(steps_num)))
        while epoch_loss > self.gate_loss:
            epoch_st = time.time()
            epoch_ind += 1
            bar = tqdm(steps_num)
            for i in bar:
                inp = self.inp_tensors[(i-1)*self.batch_size:i*self.batch_size]
                targ = self.targ_tensors[(i-1)*self.batch_size:i*self.batch_size]
                batch_loss = train_step(
                    inp, targ,
                    encoder, decoder,
                    optim.SGD(encoder.parameters(), lr = 0.01),
                    optim.SGD(decoder.parameters(), lr = 0.01)
                )
                total_loss += batch_loss
                bar.set_description("Batch_loss {:.2f}".format(batch_loss))
            epoch_ed = time.time()
            epoch_loss = total_loss / len(steps_num)
            print("[+] epoch {:>3d} | loss {:.3f} | time {:.2f}s".format(epoch_ind, epoch_loss, epoch_ed - epoch_st))
            epoch_file = self.model_file[:-3] + "_" + str(epoch_ind) + ".pt"
            torch.save({ 'encoder_dict' : encoder.state_dict(), 'decoder_dict' : decoder.state_dict()}, epoch_file)
            print("[+] saved epoch {}.".format(epoch_ind))
            total_loss = 0
        torch.save({
            'encoder_dict' : encoder.state_dict(),
            'decoder_dict' : decoder.state_dict()
        }, self.model_file)

        sys.stdout.flush()

    def __tensorFromSentence(dic, sentence):
        indexes = [dic.word2index[w] for w in sentence.split()]

    def predict(self, sentence, load_model_file = None):
        if load_model_file != None:
            print("[+] load former model file {}".format(load_model_file))
            self.model_file = load_model_file
        
        result = ''
        if not self.inp_recorder or not os.path.exists(self.model_file):
            print("[+] you should run trainer first.")
            exit()
        encoder = Encoder(self.inp_recorder.n_word, self.hidden_size).to(self.device)
        decoder = AttentionDecoder(self.hidden_size, self.out_recorder.n_word, dropout_p = 0.1).to(self.device)
        check_point = torch.load(self.model_file, map_location = self.device)
        encoder.load_state_dict(check_point['encoder_dict'])
        decoder.load_state_dict(check_point['decoder_dict'])

        sentence = sentenceCutter(sentence).strip()
        if sentence == "":
            print("[+] input sentence wrong!")
            exit()
        sentence = "ST " + sentence + " ED"
        inp_tensor = tensor_from_sentence(self.inp_recorder, sentence)

        inp_len = inp_tensor.size()[0]
        encoder_hidden = encoder.initHidden()
        encoder_outputs = torch.zeros(self.max_length, encoder.hidden_size, device = self.device)
        for ei in range(inp_len):
            encoder_output, encoder_hidden = encoder(
                inp_tensor[ei],
                encoder_hidden
            )
            encoder_outputs[ei] += encoder_output[0, 0]
        
        decoder_input = torch.tensor([[self.ST_token]], device = self.device)
        decoder_hidden = encoder_hidden
        for t in range(self.max_length):
            predictions, decoder_hidden, decoder_attns = decoder(
                decoder_input,
                decoder_hidden,
                encoder_outputs
            )
            _, topi = predictions.data.topk(1)
            if topi.item() == self.ED_token:
                result += '<END>'
                break
            else:
                result += self.out_recorder.index2word[topi.item()] + ' '
            decoder_input = topi.squeeze().detach()
        return result