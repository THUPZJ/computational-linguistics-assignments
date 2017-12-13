# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
# from pairwise_mutual_information import mut_all_file_data_preprocessing
from pairwise_mutual_information import mut_all_file_data_preprocessing
# from mean_variance_based import get_file_list
from mean_variance_based import get_file_list
from mean_variance_based import str_processing
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')


def count_bigram_dict(bigram_dict):
    bigram_sum = 0
    for ite in bigram_dict:
        bigram_sum += int(bigram_dict[ite])
    return bigram_sum


def t_test(unigram_dict, bigram_dict, xword, yword, bigram_sum):
    if xword+" "+yword not in bigram_dict or xword not in unigram_dict or yword not in unigram_dict:
        return 10
    pxword = float(unigram_dict[xword]) / bigram_sum
    pyword = float(unigram_dict[yword]) / bigram_sum
    mu = pxword * pyword
    xmean = float(bigram_dict[xword+" "+yword]) / bigram_sum
    sam_vari = xmean
    return (xmean - mu) / np.sqrt(sam_vari/bigram_sum)


def ttest_data_processing(dir_path, file_path, unigram_dict, bigram_dict, bigram_sum, ttest_info_dict):
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
                    ttest_info = t_test(unigram_dict, bigram_dict, strs[i], strs[i+1], bigram_sum)
                    if strs[i]+" "+strs[i+1] not in ttest_info_dict:
                        ttest_info_dict[strs[i]+" "+strs[i+1]] = ttest_info
                else:
                    break


def mut_all_file_data_processing(dirpath1, dirpath2, dirpath3, files1, files2, files3, unigram_dict, bigram_dict, bigram_sum, ttest_info_dict):
    for file_path in files1:
        ttest_data_processing(dirpath1, file_path, unigram_dict, bigram_dict, bigram_sum, ttest_info_dict)
    for file_path in files2:
        ttest_data_processing(dirpath2, file_path, unigram_dict, bigram_dict, bigram_sum, ttest_info_dict)
    for file_path in files3:
        ttest_data_processing(dirpath3, file_path, unigram_dict, bigram_dict, bigram_sum, ttest_info_dict)


if __name__ == '__main__':
    path1 = "/Users/datamining/Desktop/CL_4th/test"
    path2 = "/Users/datamining/Desktop/CL_4th/train"
    path3 = "/Users/datamining/Desktop/CL_4th/valid"
    files1 = get_file_list(path1)
    files2 = get_file_list(path2)
    files3 = get_file_list(path3)
    sen_flag = "。？！：；，“”、』》（）《的和不在还了一对未也大地是几有上名为有一比之又这多次于".decode('utf-8')
    unigram_token_dict = {}
    bigram_token_dict = {}
    mut_all_file_data_preprocessing(path1, path2, path3, files1, files2, files3, unigram_token_dict, bigram_token_dict)
    bigram_sum = count_bigram_dict(bigram_token_dict)

    ttest_info_dict = {}
    mut_all_file_data_processing(path1, path2, path3, files1, files2, files3, unigram_token_dict, bigram_token_dict, bigram_sum, ttest_info_dict)
    dict_result_2nd = {}
    for ite in ttest_info_dict:
        # print 'ite is :', ite
        strs = ite.split()
        if len(strs) < 2 or strs[0] in sen_flag or strs[1] in sen_flag:
            pass
        else:
            dict_result_2nd[ite] = ttest_info_dict[ite]
    dict_result = sorted(dict_result_2nd.iteritems(), key=lambda d: d[1], reverse=True)
    # dict = sortedDictValues1(token_dictionary)
    print dict_result[0:100]

    with open('/Users/datamining/Desktop/tetst_info.txt', 'w') as f:
        for ite in dict_result:
            f.write(ite[0] + ' ' + str(ite[1]) + '\n')