# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
# from frequency_based import dict_refine
from mean_variance_based import get_file_list
from mean_variance_based import str_processing
import codecs
import os
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')
'''def get_dictionary_from_txt_file(file_path):
    storage_dictionary = {}
    if not os.path.isdir(file_path):
        f = open(file_path)
        iter_f = iter(f)
        for line in iter_f:
            line = line.decode('utf-8')
            print line
            strs = line.split()
            storage_dictionary[strs[0]] = int(strs[1])
    return storage_dictionary


def get_dictionary_2_from_txt_file(file_path):
    storage_dictionary = {}
    if not os.path.isdir(file_path):
        f = open(file_path)
        iter_f = iter(f)
        for line in iter_f:
            line = line.decode('utf-8')
            print line
            strs = line.split()
            storage_dictionary[strs[0]+" "+strs[1]] = int(strs[2])
    return storage_dictionary
'''


def cal_mutual_info(unigram_sum, bigram_sum, xword, yword, unigram_dict, bigram_dict):
    #return np.log2(float(bigram_dict[xword+" "+yword])/bigram_sum/(float(unigram_dict[xword])/unigram_sum*float(unigram_dict[yword])/unigram_sum))
    if xword+" "+yword not in bigram_dict or xword not in unigram_dict or yword not in unigram_dict:
        return 0
    pxy = float(bigram_dict[xword+" "+yword]) / bigram_sum
    # print "xword is :", xword
    px = float(unigram_dict[xword]) / unigram_sum
    py = float(unigram_dict[yword]) / unigram_sum
    return np.log2(pxy) - np.log2(px) - np.log2(py)


def mut_data_preprocessing(dir_path, file_path, unigram_token_dict, bigram_token_dict):
    if not os.path.isdir(file_path):
        f = codecs.open(dir_path+"/"+file_path, encoding='gb18030', errors='replace')
        iter_f = iter(f)
        for line in iter_f:
            # line = line.decode('gb18030')
            # temp_token = {}
            # line = str_processing(line)
            tem_strs = []
            strs = line.split()
            for i in range(len(strs)):
                 tem_strs.append(str_processing(strs[i]))
            strs = tem_strs
            '''temp_strs = []
            for str in strs:
                if str not in sen_flag:
                    temp_strs.append(str)
            strs = temp_strs'''
            len_strs = len(strs)
            for i in range(len_strs):
                if strs[i] not in unigram_token_dict:
                    unigram_token_dict[strs[i]] = 1
                else:
                    unigram_token_dict[strs[i]] += 1

                if i+1 < len_strs:
                    if strs[i] + " " + strs[i+1] not in bigram_token_dict:
                        bigram_token_dict[strs[i] + " " + strs[i+1]] = 1
                    else:
                        bigram_token_dict[strs[i] + " " + strs[i + 1]] += 1


def mut_all_file_data_preprocessing(dirpath1, dirpath2, dirpath3, files1, files2, files3, unigram_token_dict, bigram_token_dict):
    for file_path in files1:
        mut_data_preprocessing(dirpath1, file_path, unigram_token_dict, bigram_token_dict)
    for file_path in files2:
        mut_data_preprocessing(dirpath2, file_path, unigram_token_dict, bigram_token_dict)
    for file_path in files3:
        mut_data_preprocessing(dirpath3, file_path, unigram_token_dict, bigram_token_dict)


def mut_data_processing(dir_path, file_path, unigram_dict, bigram_dict, sen_flag, unigram_sum, bigram_sum, mut_info_dict):
    # final_mean_vari_dict = {}
    if not os.path.isdir(file_path):
        f = codecs.open(dir_path+"/"+file_path, encoding='gb18030', errors='replace')
        iter_f = iter(f)
        for line in iter_f:
            # line = line.decode('gb18030')
            line = str_processing(line)
            tem_strs = []
            strs = line.split()
            for i in range(len(strs)):
                tem_strs.append(str_processing(strs[i]))
            strs = tem_strs
            '''temp_strs = []
            for str in strs:
                if str not in sen_flag:
                    temp_strs.append(str)
            strs = temp_strs'''
            len_strs = len(strs)
            for i in range(len_strs):
                if i+1 < len_strs:
                    # print "xword is :", strs[i], "yword is :", strs[i+1]
                    mut_info = cal_mutual_info(unigram_sum, bigram_sum, strs[i], strs[i+1], unigram_dict, bigram_dict)
                    if strs[i]+" "+strs[i+1] not in mut_info_dict:
                        mut_info_dict[strs[i]+" "+strs[i+1]] = mut_info
                else:
                    break


def mut_all_file_data_processing(dirpath1, dirpath2, dirpath3, files1, files2, files3, unigram_dict, bigram_dict, sen_flag, unigram_sum, bigram_sum, mut_info_dict):
    for file_path in files1:
        mut_data_processing(dirpath1, file_path, unigram_dict, bigram_dict, sen_flag, unigram_sum, bigram_sum, mut_info_dict)
    for file_path in files2:
        mut_data_processing(dirpath2, file_path, unigram_dict, bigram_dict, sen_flag, unigram_sum, bigram_sum, mut_info_dict)
    for file_path in files3:
        mut_data_processing(dirpath3, file_path, unigram_dict, bigram_dict, sen_flag, unigram_sum, bigram_sum, mut_info_dict)


def unigram_dict_refine(unigram_dict, sen_flag):
    unigram_dict_re = {}
    for ite in unigram_dict:
        if ite not in sen_flag:
            unigram_dict_re[ite] = unigram_dict[ite]
    return unigram_dict_re


if __name__ == "__main__":
    path1 = "/Users/datamining/Desktop/CL_4th/test"
    path2 = "/Users/datamining/Desktop/CL_4th/train"
    path3 = "/Users/datamining/Desktop/CL_4th/valid"
    files1 = get_file_list(path1)
    files2 = get_file_list(path2)
    files3 = get_file_list(path3)
    sen_flag = "。？！：；，“”、』》（）《的和不在还了一对未也大地是几有上名为有一比之又这多次于".decode('utf-8')



    one_gram_txt_filepath = "/Users/datamining/Desktop/1.txt"
    bi_gram_txt_filepath = "/Users/datamining/Desktop/2.txt"
    unigram_token_dict = {}
    bigram_token_dict = {}
    mut_all_file_data_preprocessing(path1, path2, path3, files1, files2, files3, unigram_token_dict, bigram_token_dict)
# print "埃里卡特 is ：", unigram_token_dict["埃里卡特"]
# print bigram_token_dict
    sen_flag = "。？！：；，“”、』》（）《的和不在还了一对未也大地是几有上名为有一比之又这多次于".decode('utf-8')
# bigram_token_dict = dict_refine(bigram_token_dict, sen_flag)
# unigram_token_dict = unigram_dict_refine(unigram_token_dict, sen_flag)

    mut_info_dict = {}
    unigram_sum = 0
    bigram_sum = 0

    print unigram_token_dict
    print bigram_token_dict
    for ite in unigram_token_dict:
        unigram_sum += int(unigram_token_dict[ite])
    for ite in bigram_token_dict:
        bigram_sum += int(bigram_token_dict[ite])


    mut_all_file_data_processing(path1, path2, path3, files1, files2, files3, unigram_token_dict, bigram_token_dict, sen_flag, unigram_sum, bigram_sum, mut_info_dict)
    dict_result_2nd = {}
    for ite in mut_info_dict:
        # print 'ite is :', ite
        strs = ite.split()
        if len(strs) < 2 or strs[0] in sen_flag or strs[1] in sen_flag:
            pass
        else:
            dict_result_2nd[ite] = mut_info_dict[ite]
    dict_result = sorted(dict_result_2nd.iteritems(), key=lambda d: d[1], reverse=True)
    # dict = sortedDictValues1(token_dictionary)
    print dict_result[0:100]

    with open('/Users/datamining/Desktop/mut_info2.txt', 'w') as f:
        for ite in dict_result:
            f.write(ite[0]+' '+str(ite[1]) + '\n')

