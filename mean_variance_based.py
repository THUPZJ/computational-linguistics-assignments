# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')


def get_file_list(file_path):
    files_path = os.listdir(file_path)
    # print(files_path)
    return files_path


def data_preprocessing(dir_path, file_path, token_dict, sen_flag):
    if not os.path.isdir(file_path):
        f = codecs.open(dir_path+"/"+file_path, encoding='gb18030', errors='replace')
        iter_f = iter(f)
        for line in iter_f:
            #line = line.decode('gb18030')
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
                for j in range(4):
                    if i+j+1 < len_strs:
                        if (strs[i] + " " + strs[i+j+1], j+1) not in token_dict:
                            token_dict[(strs[i] + " " + strs[i+j+1], j+1)] = 1
                        else:
                            token_dict[(strs[i] + " " + strs[i+j+1], j+1)] += 1

                    if i-j-1 >= 0:
                        if (strs[i] + " " + strs[i-j-1], -j-1) not in token_dict:
                            token_dict[(strs[i] + " " + strs[i-j-1], -j-1)] = 1
                        else:
                            token_dict[(strs[i] + " " + strs[i-j-1], -j-1)] += 1



def data_processing(dir_path, file_path, tokendict,token_mean_vari_dict , sen_flag):
    # final_mean_vari_dict = {}
    if not os.path.isdir(file_path):
        f = codecs.open(dir_path+"/"+file_path,encoding='gb18030', errors='replace')
        iter_f = iter(f)
        for line in iter_f:
            # line = line.decode('gb18030')
            line = str_processing(line)
            tem_strs = []
            strs = line.split()
            for i in range(len(strs)):
                tem_strs.append(str_processing(strs[i]))
            strs = tem_strs
            temp_strs = []
            for str in strs:
                if str not in sen_flag:
                    temp_strs.append(str)
            strs = temp_strs
            len_strs = len(strs)
            for i in range(len_strs):
                for j in range(4):
                    if i+j+1 < len_strs:
                        temp_mean, temp_vari, temp_count_sum = calculate_mean_and_variance(tokendict, strs[i]+" "+strs[i+j+1])
                        if (strs[i]+" "+strs[i+j+1], temp_mean, temp_vari) not in token_mean_vari_dict:
                            token_mean_vari_dict[(strs[i]+" "+strs[i+j+1], temp_mean, temp_vari)] = temp_count_sum
                    else:
                        break


def all_file_data_processing(dirpath1, dirpath2, dirpath3, files1, files2, files3, token_dict, token_mean_vari_dict, punctuation):
    for file_path in files1:
        data_processing(dirpath1, file_path, token_dict, token_mean_vari_dict, punctuation)
    for file_path in files2:
        data_processing(dirpath2, file_path, token_dict, token_mean_vari_dict, punctuation)
    for file_path in files3:
        data_processing(dirpath3, file_path, token_dict, token_mean_vari_dict, punctuation)



def all_file_data_preprocessing(dirpath1, dirpath2, dirpath3, files1, files2, files3, token_dict, punctuation):
    for file_path in files1:
        data_preprocessing(dirpath1, file_path, token_dict, punctuation)
    for file_path in files2:
        data_preprocessing(dirpath2, file_path, token_dict, punctuation)
    for file_path in files3:
        data_preprocessing(dirpath3, file_path, token_dict, punctuation)


def calculate_mean_and_variance(token_dict, bi_words):
    distance_sum = 0
    count_sum = 0
    # strs = bi_words.split()
    for i in range(4):
        if (bi_words, i+1) in token_dict:
            distance_sum += (token_dict[(bi_words, i+1)]*(i+1))
            count_sum += token_dict[(bi_words, i+1)]
        if (bi_words, -i-1) in token_dict:
            distance_sum += (token_dict[(bi_words, -i-1)] * (-i-1))
            count_sum += token_dict[(bi_words, -i-1)]
    mean = distance_sum / float(count_sum+0.1)
    temp = 0
    for i in range(4):
        if (bi_words, i+1) in token_dict:
            temp += (token_dict[(bi_words, i+1)] * np.square(i+1-mean))
        if (bi_words, -i-1) in token_dict:
            temp += (token_dict[(bi_words, -i-1)] * np.square(-i-1-mean))
    # print "count_sum is:", count_sum
    if count_sum == 1:
        count_sum += 0.1
    temp = temp / float(count_sum - 1)
    variance = np.sqrt(temp)
    return mean, variance, count_sum


def str_processing(str):
    index = str.rfind('/')
    begin = 0
    if str[0] == '[':
        begin = 1
    str = str[begin:index]
    return str



if __name__ == "__main__":
    path1 = "/Users/datamining/Desktop/CL_4th/test"
    path2 = "/Users/datamining/Desktop/CL_4th/train"
    path3 = "/Users/datamining/Desktop/CL_4th/valid"
    files1 = get_file_list(path1)
    files2 = get_file_list(path2)
    files3 = get_file_list(path3)
    sen_flag = "。？！：；，“”、』》（）《的和不在还了一对未也大地是几有上名为有一比之又这多次于".decode('utf-8')

    punctuation = ['。', '，', '、', '！','；', '“', '”']
    '''strs = "。/v"
    strs = str_processing(strs)
    print strs
    if strs in punctuation:
    print True'''
    token_dict = {}
    token_mean_vari_dict = {}
    all_file_data_preprocessing(path1, path2, path3, files1, files2, files3, token_dict, sen_flag)
    all_file_data_processing(path1, path2, path3, files1, files2, files3, token_dict, token_mean_vari_dict, sen_flag)
    dict_result = sorted(token_mean_vari_dict.iteritems(), key=lambda d: d[1], reverse=True)
    # dict = sortedDictValues1(token_dictionary)
    print dict_result[0:100]

    with open('/Users/datamining/Desktop/temp.txt', 'w') as f:
        for ite in dict_result[0:100]:
            f.write(ite[0][0]+' '+str(ite[0][1])+' '+str(ite[0][2])+' '+str(ite[1])+'\n')

