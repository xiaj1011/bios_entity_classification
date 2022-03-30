import json
from transformers import BertTokenizer
from tqdm import trange
import torch
from torch.utils.data import Dataset, DataLoader
from label_util import get_entity_type_from_json
from random import randint
from load_cleanterms import CLEANTERMS
from copy import deepcopy
import numpy as np
import random


def get_line(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in f:
            yield line


class Entity_Dataset(Dataset):
    def __init__(self,
                 text_file, match_file,
                 cleanterms=None,
                 tokenizer_name="bert-base-uncased",
                 window_size=32, min_entity_length=4,
                 mask_ratio=0.15,
                 control_dict={},
                 debug=False,
                 lines=-1):

        self.debug = debug
        self.lines = lines
        if self.debug:
            if self.lines == -1:
                self.lines = 1000000
            else:
                self.lines = min(self.lines, 1000000)

        if self.lines >= 0:
            gen = get_line(text_file)
            text_lines = [next(gen) for i in range(self.lines)]
        else:
            with open(text_file, 'r', encoding="utf-8") as f:
                text_lines = f.readlines()

        if self.lines >= 0:
            gen = get_line(match_file)
            match_lines = [next(gen) for i in range(self.lines)]
        else:
            with open(match_file, 'r', encoding="utf-8") as f:
                match_lines = f.readlines()

        self.cleanterms = cleanterms
        self.mask_ratio = mask_ratio

        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name)
        self.window_size = window_size
        self.min_entity_length = min_entity_length
        self.umls_labels, self.sty2sgr = get_entity_type_from_json()
        self.control_dict = control_dict

        self.sentences = []
        self.entities = []
        self.map = []

        print(f'Generate Dataset for TEXT **{text_file}** with LABEL **{text_file}**')
        for i in trange(len(text_lines)):
            flag = False
            entities = json.loads(match_lines[i])
            for entity in entities:
                if self.filter_entity(entity):
                    flag = True
                    self.entities.append(entity)
                    self.map.append(len(self.sentences))
            if flag:
                self.sentences.append(text_lines[i])

    def __getitem__(self, idx):

        line = self.sentences[self.map[idx]]
        if not line.endswith('.'):
            line = line + ' .'
        entity = self.entities[idx]
        #print(entity)
        tokenized = self.tokenizer.tokenize(line)
        encoded = self.tokenizer.convert_tokens_to_ids(tokenized)
        index_map = [0] * len(line)
        cum = 0
        for j in range(len(tokenized)):
            token = tokenized[j]
            l = len(token)
            if "##" in token:
                l -= 2
            if cum >= len(line):
                break
            while line[cum] == ' ' or line[cum] == "\xa0" or line[cum] == "\n" or line[cum] == "\t" or line[cum] == "\xc2":
                index_map[cum] = j
                cum += 1
                if cum >= len(line):
                    break
            if token == self.tokenizer.unk_token:
                l = 1
            if cum + l <= len(line):
                index_map[cum: cum + l] = [j] * l
            cum += l
        index_map[cum:] = [j] * (len(line) - cum)

        label = ['Other']  # 预测阶段，对于没见过的术语，随机赋值一个label
        if self.cleanterms.exist(entity['phrase']):
            label = self.cleanterms.str2sty(entity['phrase'])

        entity_mark = [0] * len(encoded)
        begin = index_map[entity['begin']]
        end = index_map[entity['end']]
        entity_mark[begin: end] = [1] * (end - begin)
        entity_mark[begin] = 1

        if end - begin >= self.window_size * 2:     # 此处有bug，如果>=32*2的长度，则encoded_sentences长度大于66
            window_left = begin
            window_right = end
        else:
            window_left = begin - self.window_size + (end - begin) // 2
            window_left = 0 if window_left < 0 else window_left
            window_right = end + self.window_size - (end - begin + 1) // 2
            window_right = len(encoded) if window_right > len(
                encoded) else window_right
        padding_size = self.window_size * 2 - window_right + window_left

        encoded_sentences = [self.tokenizer.cls_token_id] + encoded[window_left: window_right] \
            + [self.tokenizer.sep_token_id] + \
            [self.tokenizer.pad_token_id] * padding_size
        entity_marks = [0] + entity_mark[window_left: window_right] + [0] * (padding_size + 1)
        if 1 not in entity_marks:
            #raise BaseException
            print(index_map)
            print(entity['begin'], entity['end'])
            print(begin, end, window_left, window_right)
            print(encoded_sentences, entity_marks, line, entity)
        masked_sentences = self.mask(encoded_sentences, entity_marks)

        if len(masked_sentences) != 66 or len(entity_marks)!= 66:
            print('idx ', self.map[idx])
            print('line ', line)
            print('entity ', entity)
            print('encoded len ', len(encoded))
            print("====invalid ", masked_sentences)
            print("====invalid2 ",entity_marks)
        #print("masked sent len ", len(masked_sentences))
        #print("entity masks len ", len(entity_marks))
        #print(label)
        labels = self.deal_label(entity, label)
        #print(labels)
        return masked_sentences, entity_marks, labels


    def __len__(self):
        return len(self.entities)

    def filter_entity(self, entity):
        string = entity['phrase']
        if 'min_entity_word_count' in self.control_dict:
            word_count = len(string.split())
            if word_count < self.control_dict['min_entity_word_count']:
                return False
        if 'max_entity_word_count' in self.control_dict:
            word_count = len(string.split())
            if word_count > self.control_dict['max_entity_word_count']:
                return False
        if 'min_entity_len' in self.control_dict:
            if len(string) < self.control_dict['min_entity_len']:
                return False
        if 'max_sgr_n' in self.control_dict:
            if self.cleanterms.str2sgr_n(string) > self.control_dict['max_sgr_n']:
                return False
        if 'max_sty_n' in self.control_dict:
            if self.cleanterms.str2sty_n(string) > self.control_dict['max_sty_n']:
                return False
        if 'min_sty_n' in self.control_dict:
            if self.cleanterms.str2sty_n(string) < self.control_dict['min_sty_n']:
                return False
        if 'no_short_upper' in self.control_dict:
            if self.control_dict['no_short_upper']:
                if self.cleanterms.is_short_upper(string):
                    return False
        return True

    def deal_label(self, entity, label):
        if 'only_one' in self.control_dict:
            if self.control_dict['only_one']:
                label = random.sample(label, 1)
        list_labels = [0] * len(self.umls_labels)
        for l in label:
            list_labels[self.umls_labels[l]] = 1
        return list_labels

    def mask(self, encoded_sentences, entity_marks):
        if self.mask_ratio == 0.0:
            return encoded_sentences

        encoded_sentences = np.array(encoded_sentences)
        entity_marks = np.array(entity_marks)
        sample_count = sum(entity_marks)
        mask = np.random.rand(sample_count) < self.mask_ratio
        masked_sentences = encoded_sentences
        masked_sentences[np.arange(encoded_sentences.shape[0])[entity_marks == 1][mask]] = self.tokenizer.mask_token_id
        return masked_sentences.tolist()



def my_collate_fn(batch):
    type_count = len(batch[0])
    batch_size = len(batch)
    output = ()
    for i in range(type_count):
        tmp = [item[i] for item in batch]
        if len(tmp) <= batch_size:
            output += (torch.LongTensor(tmp),)
        else:
            output += (torch.LongTensor(tmp).reshape(batch_size, -1),)
    return output


if __name__ == "__main__":
    text_file = 'example/data/corpus.txt'
    match_file = 'example/data/corpus_tagged.txt'
    clean_term_path = 'example/cleanterms/cleanterms.txt.example'
    tokenizer_name = 'pretrain/pubmedbert_abs'
    cleanterms = CLEANTERMS(clean_term_path)
    predict_control_dict = {}
    
    predict_dataset = Entity_Dataset(text_file, match_file, cleanterms, tokenizer_name, mask_ratio=0.0, control_dict=predict_control_dict)
    for ds in predict_dataset:
        print(len(ds))
        #print(ds[0])     

#if __name__ == "__main__":
#    text_file = '/raid/tanwei/codes/term-discovery/clean_data/all_data_for_model_v2.txt'
#    match_file = '/raid/tanwei/codes/term-discovery/entity_match/all_data_for_model_v2_tagged.txt'
#    #text_file = './sample_data/text_100.txt'
#    #match_file = './sample_data/match_100.txt'
#    clean_term_path = './dict/cleanterms4.txt'
#    tokenizer_name = 'microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract'
#    cleanterms = CLEANTERMS(clean_term_path)
#    train_control_dict = {'max_sgr_n':1, 'no_short_upper':True, 'only_one':True}
#    single_eval_control_dict = {'max_sty_n':1, 'no_short_upper':True}
#    multi_eval_control_dict = {'min_sty_n':2, 'no_short_upper':True}
#    predict_control_dict = {}
#
#    train_dataset = Entity_Dataset(text_file, match_file, cleanterms, tokenizer_name, mask_ratio=0.15, control_dict=train_control_dict, debug=True)
#    single_eval_dataset = Entity_Dataset(text_file, match_file, cleanterms, tokenizer_name, mask_ratio=0.0, control_dict=single_eval_control_dict, debug=True)
#    multi_eval_dataset = Entity_Dataset(text_file, match_file, cleanterms, tokenizer_name, mask_ratio=0.0, control_dict=multi_eval_control_dict, debug=True)
#    predict_dataset = Entity_Dataset(text_file, match_file, cleanterms, tokenizer_name, mask_ratio=0.0, control_dict=predict_control_dict, debug=True)
#
#    for dataset in [train_dataset, single_eval_dataset, multi_eval_dataset, predict_dataset]:
#    # for dataset in [train_dataset]:
#        print(len(dataset))
#        print(dataset[0])
#        for i in range(len(dataset)):
#            k = dataset[i]
#        # import ipdb
#        # ipdb.set_trace()
