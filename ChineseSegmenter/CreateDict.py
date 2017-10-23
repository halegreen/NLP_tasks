#encoding=utf-8
'''
functon: Create 1-gram and 2-gram probability dict
input: file.txt
output: dict_1_gram.txt dict_2_gram.txt
@author: shaw, 2017-10-23
'''

import os
import math
import re

class Dictionary:
    def __init__(self, input_file):
        self.total_word_count = 0
        self.count_1_gram = {}   ##记录词频
        self.dict_1_gram = {}   ##记录概率
        self.count_2_gram = {}
        self.dict_2_gram = {}

        cleaned_file = []
        with open(input_file, 'r', encoding='utf-8') as f:
            file_lines = [line.strip() for line in f.readlines()]

        for line in file_lines:
            cleaned_file.append(self.clean_helper(line))

        # for line in cleaned_file:
        #     print(line)

        self.create_1_gram_dict(cleaned_file)
        self.create_2_gram_dict(cleaned_file)
        self.create_test_file(cleaned_file)


    def create_1_gram_dict(self, cleaned_file):

        for line in cleaned_file:
            for word in line:
                if not self.count_1_gram.__contains__(word):
                    self.count_1_gram[word] = 1
                else:
                    self.count_1_gram[word] += 1

        self.total_word_count = sum(self.count_1_gram.values())  ## total_word_dict = 6475111

        for key, value in self.count_1_gram.items():
            ## the minimum 1-gram prob is very small: 1.5443750694003548e-07
            self.dict_1_gram[key] = value / self.total_word_count


    def clean_helper(self, line):
        res = line.split(' ')[1:]
        res = [word.split('/')[0] for word in res if len(word) > 0]
        res = [word for word in res if 0x4e00 <= ord(word[0]) < 0x9fa6]
        return ' '.join(res).strip()


    def create_2_gram_dict(self, cleaned_file):

        pass


    def create_test_file(self, cleaned_file):
        test_file = []
        for line in cleaned_file:
            new_line = ''
            for word in line:
                new_line += word.strip()
            # print(new_line)
            test_file.append(new_line)

        with open('test_file.txt', 'w', encoding='utf-8') as f:
            f.writelines(test_file)


if __name__ == '__main__':
    d = Dictionary('199801.txt')
