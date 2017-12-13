# !/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
# import matplotlib.pyplot as plt
from held_out_estimation import count_token_from_file_list_two
from ngram_test_generate_txt_file import count_token_from_file_list #this is from 3 different file directory
from count_tokens import get_file_list
from adding_lambd import get_one_gram_dict_from_file
from count_tokens import count_token_from_txt_file
# from count_tokens import count_token_from_file_list
import count_tokens
# import adding_lambd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def good_turing_estimation(one_word_count, two_words, token_dict):
    Nr = 0
    Nr_1 = 0
    N1 = 0
    N = len(token_dict)
    if two_words in token_dict:
        r = token_dict[two_words]
        for ite in token_dict:
            if token_dict[ite] == r:
                Nr += 1
            if token_dict[ite] == r + 1:
                Nr_1 += 1
        return np.log10(float((r + 1) * float(Nr_1) / float(Nr) / float(N)))
    else:
        N0 = one_word_count * one_word_count - N
        for ite in token_dict:
            if token_dict[ite] == 1:
                N1 += 1
        return np.log10(N1 / float((N0 * N)))


def prob_one_gram(one_gram_dict, one_word):
    one_gram_total_count = 0
    for ite in one_gram_dict:
        one_gram_total_count += one_gram_dict[ite]
    # print "one_word is :", one_word
    return np.log10(one_gram_dict[one_word]/float(one_gram_total_count))


'''def good_turing_estimation(one_word, token_dict):
    r = 0
    Nr = 0
    N0 = 0
    N1 = 0
    N = len(token_dict)
    if one_word in token_dict:
        r = token_dict[one_word]
        for ite in token_dict:
            if token_dict[ite] == r:
                Nr += 1
        return (r + 1) / r * Nr / N
    else:
        N0 = one_word_count * one_word_count - N
        for ite in token_dict:
            if token_dict == 1:
                N1 += 1
        return N1 / (N0 * N)
    pass'''


def count_token_from_file_list_two_one_gram(path1, path2, files1,files2, token_dict_one_word):
    for file_path1 in path1:
        count_token_from_txt_file(file_path1, files1, token_dict_one_word)
    for file_path2 in path2:
        count_token_from_txt_file(file_path2, files2, token_dict_one_word)


def calculate_sentence_prob_part(sentence, one_gram_dict, two_gram_dict, two_gram_start_dict, two_gram_end_dict):
    strs = sentence.split()
    one_gram_prob = []
    two_gram_prob = []
    len_of_sen = len(strs)
    for i in range(len_of_sen - 1):
        if i != 0 and i < len_of_sen - 1:
            one_gram_prob.append(prob_one_gram(one_gram_dict, strs[i]))
        if i == 0:
            two_gram_prob.append(good_turing_estimation(len(one_gram_dict), strs[i] + " " + strs[i + 1], two_gram_start_dict))
        elif i == len_of_sen-2:
            two_gram_prob.append(good_turing_estimation(len(one_gram_dict), strs[i] + " " + strs[i + 1], two_gram_end_dict))
        else:
            two_gram_prob.append(good_turing_estimation(len(one_gram_dict), strs[i] + " " + strs[i + 1], two_gram_dict))
    return one_gram_prob, two_gram_prob


def calculate_sentence_prob(one_gram_prob, two_gram_prob):
    prob = 0
    for i in range(len(one_gram_prob)):
        prob -= one_gram_prob[i]
    for i in range(len(two_gram_prob)):
        prob += two_gram_prob[i]
    return prob

if __name__ == '__main__':
    one_gram_txt_filepath = "/Users/datamining/Desktop/1.txt"
    path1 = "/Users/datamining/Desktop/CL_4th/test"
    path2 = "/Users/datamining/Desktop/CL_4th/train"
    path3 = "/Users/datamining/Desktop/CL_4th/valid"
    files1 = get_file_list(path1)
    files2 = get_file_list(path2)
    files3 = get_file_list(path3)


    token_dict_train_valid = {}
    sen_start_dict_train_valid = {}
    sen_end_dict_train_valid = {}
    one_gram_token_train_valid = {}

    token_dict_all3 = {}
    sen_start_dict_all3 = {}
    sen_end_dict_all3 = {}
    one_gram_token_all3 = get_one_gram_dict_from_file(one_gram_txt_filepath)

    sen_flag = "。？！：；".decode('utf-8')
    count_token_from_file_list_two(path2, path3, files2, files3, token_dict_train_valid, sen_start_dict_train_valid, sen_end_dict_train_valid, sen_flag, one_gram_token_train_valid)
    count_token_from_file_list(path1, path2, path3, files1, files2, files3, token_dict_all3, sen_start_dict_all3, sen_end_dict_all3, sen_flag)


    token_dict_one_word_all3 = {}
    count_tokens.count_token_from_file_list(path1, path2, path3, files1, files2, files3, token_dict_one_word_all3)
    one_word_count = len(token_dict_one_word_all3)

    one_gram_prob_train_valid = []
    two_gram_prob_train_valid = []
    prob_train_valid = 0

    one_gram_prob_all3 = []
    two_gram_prob_all3 = []
    prob_all3 = 0

    sentence = "<BOS> 国立 西南 联合 大学 是 世界 一流 大学 <EOS>"
    sentence = sentence.decode('utf-8')

    one_gram_prob_train_valid, two_gram_prob_train_valid = calculate_sentence_prob_part(sentence, one_gram_token_train_valid, token_dict_train_valid, sen_start_dict_train_valid, sen_end_dict_train_valid)
    prob_train_valid = calculate_sentence_prob(one_gram_prob_train_valid, two_gram_prob_train_valid)
    print "one_gram_prob_train_valid is :", one_gram_prob_train_valid
    print "two_gram_prob_train_valid is :", two_gram_prob_train_valid
    print "prob_train_valid is :", prob_train_valid

    one_gram_prob_all3, two_gram_prob_all3 = calculate_sentence_prob_part(sentence, token_dict_one_word_all3, token_dict_all3, sen_start_dict_all3, sen_end_dict_all3)
    prob_all3 = calculate_sentence_prob(one_gram_prob_all3, two_gram_prob_all3)
    print "one_gram_prob_all3 is :", one_gram_prob_all3
    print "two_gram_prob_all3 is :", two_gram_prob_all3
    print "prob_all3 is :", prob_all3
