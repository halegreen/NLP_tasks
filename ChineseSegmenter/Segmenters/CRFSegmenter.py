#encoding=utf-8
'''
functon: Create segmenter, based on CRF method
input: dict
output: segmented file
@author: shaw, 2017-10-26
'''

from ChineseSegmenter.Segmenters import BaseSegmenter





class CRFSegmenter(BaseSegmenter.BaseSegmenter):

    def __init__(self):
        super(CRFSegmenter, self).__init__()
        pass

    def __segment(self):
        pass