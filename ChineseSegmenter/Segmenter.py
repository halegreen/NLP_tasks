#encoding=utf-8
'''
functon: Create segmenter
input: dict
output: segmented file
@author: shaw, 2017-10-24
'''

import sys
import math
from ChineseSegmenter.CreateDict import Dictionary

class Segmenter:
    def __init__(self):
        self.word_dict = Dictionary('199801.txt')
        self.node_list_states = []
        self.node_prob_map = {}


    def get_candidate_word(self, sequence):
        '''
        :function:求待切分字串的所有候选词
        '''
        candidate_sequence = []
        i = 0
        while i < len(sequence):
            word_len = 1
            while word_len <= self. word_dict.max_word_length:
                candidate_word = {}
                word = sequence[i: i + word_len]
                if self.word_dict.dict_1_gram.__contains__(word):
                    word_freq = self.word_dict.dict_1_gram[word]
                elif self.word_dict.dict_2_gram.__contains__(word):
                    word_freq = self.word_dict.dict_2_gram[word]
                elif len(word) == 1:
                    word_freq = 0
                else:
                    word_len += 1
                    continue
                candidate_word['word'] = word
                candidate_word['word_freq'] = word_freq
                candidate_word['pos'] = i
                candidate_word['length'] = len(word)
                if candidate_word in candidate_sequence:
                    word_len += 1
                    continue
                candidate_sequence.append(candidate_word)
                word_len += 1
            i += 1

        return candidate_sequence


    def get_acc_prob(self, sequence):
        for i in range(len(sequence)):
            if i == 0:
                prob = sequence[i]['word_freq']
            else:
                prev_node_dix = i - 1
                comb_word = sequence[prev_node_dix]['word'] + sequence[i]['word']
                prob = sequence[i]['word_freq'] * self.get_2_gram_prob(comb_word)  ## 累积概率
            if not self.node_prob_map.__contains__(i):
                self.node_prob_map[i] = prob


    def get_best_prev_node_2(self, sequence, node_idx):
        prev_node_list = []
        if sequence[node_idx]['pos'] == 0:
            best_prev_node = -1
            cur_prob = sequence[node_idx]['word_freq']
            prev_node_list.append((best_prev_node, cur_prob))
        else:
            for word_idx in range(node_idx):
                if sequence[word_idx]['pos'] + sequence[word_idx]['length'] == sequence[node_idx]['pos']:
                    prev_node_list.append((word_idx,
                                           self.node_prob_map[word_idx]))

        best_prev_node, cur_prob = max(prev_node_list, key=lambda x: x[1])
        return (best_prev_node, cur_prob)



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
            ## === 这里需要修改 ===
            prob = self.get_unkonw_word_prob(word, 2)
        return prob


    def get_unkonw_word_prob(self, word, gram):
        if gram == 1:
            return math.log(10. / self.word_dict.total_word_count * 10 ** len(word))
            # return 0
        else:
            return math.log(10. / self.word_dict.total_word_count * 10 ** len(word))
            # return 0


    ## bug exist
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
        # ## 加入头结点
        # first_state = {}
        # first_state['best_prev_node'] = -1
        # first_state['cur_prob'] = 0

        prev_node_map = {}
        ## 计算每个结点的最优左邻点
        for node in range(0, len(sequence)):
            # node = sequence[node_idx]['pos']
            best_prev_ndoe, cur_prob = self.get_best_prev_node_2(sequence, node)
            prev_node_map[node] = best_prev_ndoe
            print("node: " + str(node) + " " + "best prev node: " + str(best_prev_ndoe))

        ## 得到最大概率的划分序列
        ## 确定终点词的序号
        end_word = len(sequence) - 1
        end_freq = sequence[end_word]['word_freq']
        for i in range(len(sequence)):
            if sequence[i]['pos'] + sequence[i]['length'] == len(sequence):
                if sequence[i]['freq'] > end_freq:
                    print(end_word, end_freq)
                    end_word = i
                    end_freq = sequence[i]['word_freq']
        print("end word : " + str(end_word))

        seg_sequence = ""
        word_index = end_word
        while word_index >= 0:
            seg_sequence = sequence[word_index]['word'] + " " + seg_sequence
            word_index = prev_node_map[word_index]

        # seg_index = []
        # node_idx = sequence[len(sequence) - 1]['pos']
        # seg_index.append(node_idx)
        # while node_idx is not -1:
        #     prev_node = prev_node_map[node_idx]
        #     if prev_node == -1:
        #         break
        #     seg_index.append(prev_node)
        #     node_idx = prev_node
        # seg_index.reverse()
        # ##
        # seg_sequence = []
        # for i in range(len(seg_index)):
        #     for j in range(len(sequence)):
        #         if sequence[j]['pos'] == i:
        #             final_word = sequence[j]['word']
        #     seg_sequence.append(final_word)
        # seg_sequence = ' '.join(seg_sequence)
        return seg_sequence



if __name__ == '__main__':
    # seqeunce = input("请输入待切分的句子：")
    sequence = "他们有意见分歧"
    sg = Segmenter()
    candidate_sq = sg.get_candidate_word(sequence)

    # for c in candidate_sq:
    #     print(c)

    sg.get_acc_prob(candidate_sq)
    seg_sq = sg.max_prob_seg(candidate_sq)
    print(seg_sq)