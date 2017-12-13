# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import sys
from ngram_experiment import get_dictionary_2_from_txt_file
reload(sys)
sys.setdefaultencoding('utf-8')


def dict_refine(dict, sen_flag):
    refine_dict = {}
    for ite in dict:
        # print ite
        strs = ite.split()
        # print strs
        if strs[0] not in sen_flag and strs[1] not in sen_flag:
            refine_dict[strs[0].decode('utf-8') + " " + strs[1].decode('utf-8')] = dict[ite]
    return refine_dict


if __name__ == '__main__':
    sen_flag = "。？！：；，“”、』》（）《的和不在还了一对未也大地是几有上名为有一比之又这多次于".decode('utf-8')
    file_path = '/Users/datamining/Desktop/2.txt'
    bigram_dict = get_dictionary_2_from_txt_file(file_path)

    refine_bigram_dict = dict_refine(bigram_dict, sen_flag)
    # print refine_bigram_dict
    bigram_dict_sorted = sorted(refine_bigram_dict.iteritems(), key=lambda d: d[1], reverse=True)
    # sen_end = sorted(sen_end_dict.iteritems(), key=lambda d: d[1], reverse=True)
    print bigram_dict_sorted[0:100]
    with open('/Users/datamining/Desktop/5.txt', 'w') as f:
        for ite in bigram_dict_sorted:
            f.write(ite[0].decode('utf-8') + '   '+str(ite[1])+'\n')
        # print ite, str(sen_start_dict[ite])
'''with open('/Users/datamining/Desktop/12.txt', 'w') as f:
    for ite in sen_end:
        f.write(ite[0].decode('utf-8') + '   '+str(ite[1])+'\n')
        # print ite[0], str(ite[1])
'''
