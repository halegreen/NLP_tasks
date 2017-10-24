#encoding=utf-8
'''
functon: Create segmenter
input: dict
output: segmented file
@author: shaw, 2017-10-24
'''

import os
import math
from ChineseSegmenter.CreateDict import Dictionary

class Segmenter:
    def __init__(self):
        self.word_dict = Dictionary('199801.txt')
        self.node_list_states = []

    def get_1_gram_prob(self, word):
        if self.word_dict.dict_1_gram.__contains__(word):
            prob = self.word_dict.dict_1_gram[word]
        else:
            prob = self.get_unkonw_word_prob(word, 1)
        return prob


    def get_2_gram_prob(self, word):
        if self.word_dict.dict_2_gram.__contains__(word):
            prob = self.word_dict.dict_2_gram[word]
        else:
            prob = self.get_unkonw_word_prob(word, 2)
        return prob


    def get_unkonw_word_prob(self, word, gram):
        if gram == 1:
            return math.log(10. / self.word_dict.total_word_count * 10 ** len(word))
        else:
            return


    def get_best_prev_node(self, sequence, node_idx):
        if node_idx in self.node_list_states:
            return (self.node_list_states[node_idx]['best_prev_node'],
                    self.node_list_states[node_idx]['cur_prob'])
        prev_node_list = []
        ## 前向计算每个词的累计概率
        for i in range(node_idx):
            if i == 0:
                prev_node = -1
                cur_prob = self.get_1_gram_prob(sequence[i])
            elif i == 1:
                prev_node = 0
                cur_prob = self.get_1_gram_prob(sequence[i])
            else:
                prev_prev_node = self.node_list_states[i]['best_prev_node']['best_prev_node']
                prev_word = sequence[prev_prev_node: i]
                cur_prob = self.get_1_gram_prob(sequence[i]) * self.get_2_gram_prob(prev_word)

            prev_node_list.append((prev_node, cur_prob))

        ## 反向寻找最佳左邻词
        best_prev_node, max_prob = max(prev_node_list, key=lambda x: x[1])
        return best_prev_node, max_prob


    def max_prob_seg(self, sequence):
        ## 加入头结点
        first_state = {}
        first_state['best_prev_node'] = -1
        first_state['cur_prob'] = 0
        self.node_list_states.append(first_state)
        ## 计算每个结点的最优左邻点
        for node_idx in range(0, len(sequence)):
            best_prev_ndoe, cur_prob = self.get_best_prev_node(sequence, node_idx)
            cur_state = {}
            cur_state['best_prev_node'] = best_prev_ndoe
            cur_state['cur_prob'] = cur_prob
        ## 得到最大概率的划分序列
        seg_index = []
        node = len(sequence)
        seg_index.append(node)
        while node is not -1:
            prev_node = self.node_list_states[node]['best_prev_node']
            if prev_node == -1:
                break
            seg_index.append(prev_node)
            node = prev_node
        seg_index.reverse()
        ##
        seg_sequence = []
        for i in range(len(seg_index)):
            seg_sequence.append(sequence[seg_index[i]])
        seg_sequence = ' '.join(seg_sequence)
        return seg_sequence



if __name__ == '__main__':
    seqeunce = input("请输入待切分的句子：")
    sg = Segmenter()
    seg_sq = sg.max_prob_seg(seqeunce)
    print(seg_sq)