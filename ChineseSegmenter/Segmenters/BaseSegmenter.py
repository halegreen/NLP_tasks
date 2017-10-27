#encoding=utf-8
'''
functon: Base segmenter
input: dict
output: segmented file
@author: shaw, 2017-10-26
'''

from ChineseSegmenter.CreateDict import Dictionary

class BaseSegmenter():
    def __init__(self):
        self.word_dict = Dictionary('data/199801.txt')

    def __segment(self):
        pass

    def __eval(self):
        pass