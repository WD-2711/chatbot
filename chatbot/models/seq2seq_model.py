#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/14 21:45:17
# @Author: wd-2711
'''

from config.config import *

config = getConfig()
max_length = config['max_length']
batch_size = config['batch_size']
ST_token = config['st_token']
ED_token = config['ed_token']
criterion = nn.NLLLoss()

class Encoder(nn.Module):
    def __init__(self, inp_size, hidd_size):
        super(Encoder, self).__init__()
        self.hidden_size = hidd_size
        self.embedding = nn.Embedding(inp_size, hidd_size)
        self.GRU = nn.GRU(hidd_size, hidd_size)

    def forward(self, input, hidden):
        embedded = self.embedding(input).view(1, 1, -1)
        output, hidden = self.GRU(embedded, hidden)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device = device)

class AttentionDecoder(nn.Module):
    def __init__(self, hidden_size, output_size, dropout_p = 0.1, max_length = max_length):
        super(AttentionDecoder, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.dropout_p = dropout_p
        self.max_length = max_length

        self.embedding = nn.Embedding(self.output_size, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.GRU = nn.GRU(self.hidden_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.out = nn.Linear(self.hidden_size, self.output_size)
    
    def forward(self, input, hidden, encoder_outputs):
        embedded = self.embedding(input).view(1, 1, -1)
        embedded = self.dropout(embedded)
        attn_weights = F.softmax(
            self.attn(torch.cat((embedded[0], hidden[0]), dim = 1)),
            dim = 1
        )
        attn_applied = torch.bmm(attn_weights.unsqueeze(0), encoder_outputs.unsqueeze(0))
        output = self.attn_combine(
            torch.cat((embedded[0], attn_applied[0]), dim = 1)
        ).unsqueeze(0)
        output = F.relu(output)
        output, hidden = self.GRU(output, hidden)
        output = F.log_softmax(self.out(output[0]), dim = 1)
        return output, hidden, attn_weights
    
    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device = device)

def train_step(inp_tensors, targ_tensors, encoder, decoder, encoder_optim, decoder_optim):
    encoder_hidden = encoder.initHidden()
    encoder_optim.zero_grad()
    decoder_optim.zero_grad()

    loss = 0
    for i in range(batch_size):
        inp_tensor = inp_tensors[i]
        targ_tensor = targ_tensors[i]
        inp_len = inp_tensor.size(0)
        targ_len = targ_tensor.size(0)
        encoder_outs = torch.zeros(max_length, encoder.hidden_size, device = device)
        
        for ei in range(min(max_length, inp_len)):
            encoder_out, encoder_hidden = encoder(
                inp_tensor[ei], 
                encoder_hidden
            )
            encoder_outs[ei] = encoder_out[0, 0]
        
        decoder_inp = torch.tensor([[ST_token]], device = device)
        decoder_hidden = encoder_hidden
        for di in range(targ_len):
            decoder_out, decoder_hidden, decoder_attn = decoder(
                decoder_inp, 
                decoder_hidden,
                encoder_outs
            )
            loss += criterion(F.log_softmax(decoder_out, dim = 1), targ_tensor[di]) / targ_len
            decoder_inp = targ_tensor[di]
    loss.backward()
    encoder_optim.step()
    decoder_optim.step()
    return loss.item() / batch_size