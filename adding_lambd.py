# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')

dir_path = None
file_path = None


def get_one_gram_dict_from_file(file_path):
    one_gram_dict = {}
    # if define one_gram_dict = None, it will cause a error: assignment can't be do on a None type
    f = open(file_path)
    iter_f = iter(f)
    for line in iter_f:
        # print line
        strs = line.split()
        # print "len of strs is :", len(strs)
        # print "strs[0] is :", strs[0]
        # print "strs[1] is :", strs[1]
        one_gram_dict[strs[0]] = int(strs[1])
    return one_gram_dict


def get_two_gram_from_file(file_path):
    two_gram_dict = None
    f = open(file_path)
    iter_f = iter(f)
    for line in iter_f:
        strs = line.split()
        two_gram_dict[strs[0] + " " + strs[1]] = int(strs[2])
    return two_gram_dict


def adding_lambda(one_gram_dict, two_gram_dict, two_words, lambd):
    N = len(one_gram_dict) * len(one_gram_dict)
    # for ite in two_gram_dict:
    #    N += two_gram_dict[ite]
    # strs = two_words.split()
    B = len(two_gram_dict)
    C = 0
    if two_words in two_gram_dict:
        C = two_gram_dict[two_words]
    return np.log10((C + lambd) / (N + B * lambd))


def adding_lambda_one_gram(one_gram_dict, one_word, lambd):
    N=0
    for ite in one_gram_dict:
        N += one_gram_dict[ite]
    B = len(one_gram_dict)
    C = 0
    if one_word in one_gram_dict:
        C = one_gram_dict[one_word]
    # return np.log10((C + lambd) / (N + B * lambd))
    return np.log10(C / float(N))


def loading_one_gram_dict_txt(file_path, one_gram_dict):
    if not os.path.isdir(file_path):
        f = open(file_path)
        iter_f = iter(f)
        for line in iter_f: # print line.decode('gb18030')
            line = line.decode('utf-8')
            strs = line.split()
            one_gram_dict[strs[0]] = int(strs[1])


def loading_two_gram_dict_txt(file_path, two_gram_dict):
    if not os.path.isdir(file_path):
        f = open(file_path)
        iter_f = iter(f)
        for line in iter_f:
            line = line.decode('utf-8') #这样之后就不会报错了
            strs = line.split()
            two_gram_dict[strs[0] + strs[1]] = int(strs[2])


def calculate_sentence_prob_part(sentence, one_gram_dict, two_gram_dict, two_gram_start_dict, two_gram_end_dict, lambd):
    strs = sentence.split()
    one_gram_prob = []
    two_gram_prob = []
    len_of_sen = len(strs)
    for i in range(len_of_sen - 1):
        if i != 0 and i < len_of_sen - 1:
            one_gram_prob.append(adding_lambda_one_gram(one_gram_dict, strs[i], lambd))
        if i == 0:
            two_gram_prob.append(adding_lambda(one_gram_dict, two_gram_start_dict, strs[i] + strs[i + 1], lambd))
        elif i == len_of_sen-2:
            two_gram_prob.append(adding_lambda(one_gram_dict, two_gram_end_dict, strs[i] + strs[i + 1], lambd))
        else:
            two_gram_prob.append(adding_lambda(one_gram_dict, two_gram_dict, strs[i] + strs[i+1], lambd))
    return one_gram_prob, two_gram_prob


def calculate_sentence_prob(one_gram_prob, two_gram_prob):
    prob = 0
    for i in range(len(one_gram_prob)):
        prob -= one_gram_prob[i]
    for i in range(len(two_gram_prob)):
        prob += two_gram_prob[i]
    return prob


if __name__ == "__main__":
    one_gram_file_path = "/Users/datamining/Desktop/1.txt"
    two_gram_file_path = "/Users/datamining/Desktop/2.txt"
    two_gram_start_file_path = "/Users/datamining/Desktop/3.txt"
    two_gram_end_file_path = "/Users/datamining/Desktop/4.txt"
    one_gram_dict = {}
    two_gram_dict = {}
    two_gram_start_dict = {}
    two_gram_end_dict = {}
    loading_one_gram_dict_txt(one_gram_file_path, one_gram_dict)
    loading_two_gram_dict_txt(two_gram_file_path, two_gram_dict)
    loading_two_gram_dict_txt(two_gram_start_file_path, two_gram_start_dict)
    loading_two_gram_dict_txt(two_gram_end_file_path, two_gram_end_dict)
    # print two_gram_dict
    two_words = "扶贫" + "开发"
    two_words = two_words.decode('utf-8')
    p_test = adding_lambda(one_gram_dict, two_gram_dict, two_words, 0.1)
    print "p_test is :", p_test
    if two_words in two_gram_dict:
        print "two_gram_dict[two_words] is:", two_gram_dict[two_words]
    else:
        print "Not existed!"
    ana_two_words = "我爱罗 沙影"
    ana_two_words = ana_two_words.decode('utf-8')
    p_ana_test = adding_lambda(one_gram_dict, two_gram_dict, ana_two_words, 0.1)
    print "p_ana_test is :", p_ana_test

    one_word = "扶贫"
    one_word = one_word.decode('utf-8')
    p_one_word = adding_lambda_one_gram(one_gram_dict, one_word, 0.1)
    print "p_one_word is :", p_one_word
    ana_one_word = "我爱罗"
    ana_two_words = ana_two_words.decode('utf-8')
    p_ana_one_word = adding_lambda_one_gram(one_gram_dict, ana_one_word, 0.1)
    print "p_ana_one_word is :", p_ana_one_word

    test_sentence = "<BOS> 国立 西南 联合 大学 是 世界 一流 大学 <EOS>"
    test_sentence = test_sentence.decode('utf-8')
    one_gram_prob, two_gram_prob = calculate_sentence_prob_part(test_sentence, one_gram_dict, two_gram_dict, two_gram_start_dict, two_gram_end_dict, float(1))
    print "one_gram_prob is :", one_gram_prob
    print "two_gram_prob is :", two_gram_prob
    prob = calculate_sentence_prob(one_gram_prob, two_gram_prob)
    print "整个句子的概率是 :", prob