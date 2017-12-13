# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
# from adding_lambd import get_one_gram_dict_from_file
# from adding_lambd import get_two_gram_from_file
from ngram_test_generate_txt_file import get_n_gram
from count_tokens import get_file_list
from count_tokens import count_token_from_txt_file
# from ngram import get_n_gram
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')


def held_out(two_gram_dict_train, two_gram_dict_heldout, two_words):
    pass


def count_token_from_file_list_two(dir_path1, dir_path2, files1, files2, token_dict, sen_start_dict, sen_end_dict, sen_flag, one_gram_dict):
    '''此处返回的是从两个数据集返回的二元文法的词典'''
    for file_path1 in files1:
        get_n_gram(dir_path1, file_path1, token_dict, sen_start_dict, sen_end_dict, sen_flag)
        count_token_from_txt_file(dir_path1, file_path1, one_gram_dict)
    for file_path2 in files2:
        get_n_gram(dir_path2, file_path2, token_dict, sen_start_dict, sen_end_dict, sen_flag)
        count_token_from_txt_file(dir_path2, file_path2, one_gram_dict)


def count_token_from_file_list(dir_path, files, token_dict, sen_start_dict, sen_end_dict, sen_flag, one_gram_dict):
    for file_path in files:
        get_n_gram(dir_path, file_path, token_dict, sen_start_dict, sen_end_dict, sen_flag)
        count_token_from_txt_file(dir_path, file_path, one_gram_dict)


def get_held_out(one_word_count, two_word, token_dict_train, token_dict_heldout):
    Tr = 0
    Nr = 0
    N = len(token_dict_train)
    r = 0
    if two_word in token_dict_train:
        r = token_dict_train[two_word]
    if r == 0:
        Nr = one_word_count * one_word_count - N
    else:
        for ite in token_dict_train:
            if token_dict_train[ite] == r:
                Nr += 1
    if r == 0:
        for ite in token_dict_heldout:
            if ite not in token_dict_train:
                Tr += token_dict_heldout[ite]
    else:
        for ite in token_dict_train:
            if token_dict_train[ite] == r:
                if ite in token_dict_heldout:
                    Tr += token_dict_heldout[ite]
    # print "one_word_count is :", one_word_count
    # print "Tr,Nr,N is :", Tr, " ", Nr, " ", N
    return np.log10(Tr / float(Nr * N))


def get_held_out_one_gram(one_word, token_dict_train, token_dict_heldout):
    Tr = 0
    Nr = 0
    N = len(token_dict_train)
    r = 0
    if one_word in token_dict_train:
        r = token_dict_train[one_word]
    if r == 0:
        for ite in token_dict_heldout:
            if ite not in token_dict_train:
                Tr += token_dict_heldout[ite]
    else:
        for ite in token_dict_train:
            if token_dict_train[ite] == r:
                Nr += 1
                if ite in token_dict_heldout:
                    Tr += token_dict_heldout[ite]
    print "Tr,Nr,N is :", Tr, " ", Nr, " ", N
    return np.log10(Tr / float(Nr * N))


def prob_one_gram(one_gram_dict, one_word):
    one_gram_total_count = 0
    for ite in one_gram_dict:
        one_gram_total_count += one_gram_dict[ite]
    # print one_gram_dict[one_word]
    return np.log10(one_gram_dict[one_word]/float(one_gram_total_count))


def calculate_sentence_prob_part(sentence, one_gram_token_dict_train, one_gram_token_dict_heldout, token_dict_train, token_dict_heldout, token_start_dict_train, token_end_dict_train, token_start_dict_heldout, token_end_dict_heldout, one_word_count):
    strs = sentence.split()
    one_gram_prob = []
    two_gram_prob = []
    len_of_sen = len(strs)
    for i in range(len_of_sen - 1):
        if i != 0 and i < len_of_sen - 1:
            one_gram_prob.append(prob_one_gram(one_gram_token_dict_train, strs[i]))
        if i == 0:
            two_gram_prob.append(get_held_out(one_word_count, strs[i] + " " + strs[i + 1], token_start_dict_train, token_start_dict_heldout))
        elif i == len_of_sen-2:
            two_gram_prob.append(
                get_held_out(one_word_count, strs[i] + " " + strs[i + 1], token_end_dict_train, token_end_dict_heldout))
        else:
            two_gram_prob.append(
                get_held_out(one_word_count, strs[i] + " " + strs[i + 1], token_dict_train, token_dict_heldout))
    return one_gram_prob, two_gram_prob


def calculate_sentence_prob(one_gram_prob, two_gram_prob):
    prob = 0
    for i in range(len(one_gram_prob)):
        prob -= one_gram_prob[i]
    for i in range(len(two_gram_prob)):
        prob += two_gram_prob[i]
    return prob
# def count_token_from_file_list_train(path1, files1, )


if __name__ == "__main__":
    path1 = "/Users/datamining/Desktop/CL_4th/test"
    path2 = "/Users/datamining/Desktop/CL_4th/train"
    path3 = "/Users/datamining/Desktop/CL_4th/valid"
    files1 = get_file_list(path1)
    files2 = get_file_list(path2)
    files3 = get_file_list(path3)
    sen_flag = "。？！：；".decode('utf-8')

    one_word_count = 0

    one_gram_token_dict_valid_test = {}
    token_dict_valid_test = {}
    sen_start_dict_valid_test = {}
    sen_end_dict_valid_test = {}

    one_gram_token_dict_train = {}
    token_dict_train = {}
    sen_start_dict_train = {}
    sen_end_dict_train = {}

    one_gram_token_dict_valid = {}
    token_dict_valid = {}
    sen_start_dict_valid = {}
    sen_end_dict_valid = {}

    count_token_from_file_list_two(path1, path3, files1, files3, token_dict_valid_test, sen_start_dict_valid_test, sen_end_dict_valid_test, sen_flag, one_gram_token_dict_valid)
    count_token_from_file_list(path2, files2, token_dict_train, sen_start_dict_train, sen_end_dict_train, sen_flag, one_gram_token_dict_train)
    count_token_from_file_list(path3, files3, token_dict_valid, sen_start_dict_valid, sen_end_dict_valid, sen_flag, one_gram_token_dict_valid)
    print "len of token_dict_valid_test is :", len(token_dict_valid_test)
    one_gram_prob_valid = []
    two_gram_prob_valid = []
    prob_valid = 0

    one_gram_prob_valid_test = []
    two_gram_prob_valid_test = []
    prob_valid_test = 0

    sentence = "<BOS> 国立 西南 联合 大学 是 世界 一流 大学 <EOS>"
    sentence = sentence.decode('utf-8')
    one_gram_prob_valid, two_gram_prob_valid = calculate_sentence_prob_part(sentence, one_gram_token_dict_train, one_gram_token_dict_valid, token_dict_train, token_dict_valid, sen_start_dict_train, sen_end_dict_train, sen_start_dict_valid, sen_end_dict_valid, len(one_gram_token_dict_train))
    prob_valid = calculate_sentence_prob(one_gram_prob_valid, two_gram_prob_valid)
    print "one_gram_prob_valid is :", one_gram_prob_valid
    print "two_gram_prob_valid is :", two_gram_prob_valid
    print "prob_valid is :", prob_valid


    one_gram_prob_valid_test, two_gram_prob_valid_test = calculate_sentence_prob_part(sentence, one_gram_token_dict_train, one_gram_token_dict_valid_test, token_dict_train, token_dict_valid_test, sen_start_dict_train, sen_end_dict_train, sen_start_dict_valid_test, sen_end_dict_valid_test, len(one_gram_token_dict_train))
    prob_valid_test = calculate_sentence_prob(one_gram_prob_valid_test, two_gram_prob_valid_test)
    print "one_gram_prob_valid_test is :", one_gram_prob_valid_test
    print "two_gram_prob_valid_test is :", two_gram_prob_valid_test
    print "prob_valid is :", prob_valid_test
