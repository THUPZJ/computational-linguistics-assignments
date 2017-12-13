# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

file_path1 = '/Users/datamining/Desktop/1.txt'
file_path2 = '/Users/datamining/Desktop/2.txt'
file_path3 = '/Users/datamining/Desktop/4.txt'
file_path4 = '/Users/datamining/Desktop/5.txt'
input1 = "扶贫 开发 工作 取得 很 大 成绩"
input2 = "扶贫 开发 工作 得到 很 大 成绩"
total_count = None

def get_file_list(file_path):
    files_path = os.listdir(file_path)
    return files_path


def get_n_gram(dir_path, file_path, token_dictionary, sen_start_dict, sen_end_dict, sen_flag):
    if not os.path.isdir(file_path):
        f = open(dir_path+"/"+file_path)
        iter_f = iter(f)
        for line in iter_f:
            # print line.decode('gb18030')
            line = line.decode('gb18030')
            start = 0
            end = 0
            whitespace = 0
            pre_previous = None
            previous = None
            current = None
            pre_is_sentence = True
            cur_is_sentence = False
            for i in range(len(line)):

                if line[i] == '[':
                    start = i+1
                if line[i] == ' ':
                    whitespace += 1
                    if whitespace == 1:
                        start = i+2
                    if whitespace == 2:
                        whitespace = 0
                if line[i] == '/':
                    end = i
                if end > start:
                    print "line[i-1] is :", line[i-1]
                    if line[i-1] in sen_flag:
                        cur_is_sentence = True
                    current = line[start: end].decode('gb18030')
                    # print "current is:" + current + "\n"
                    if previous is not None and current is not None:
                        if previous + " " + current not in token_dictionary:
                            token_dictionary[previous + " " + current] = 1
                        else:
                            token_dictionary[previous + " " + current] += 1
                        if pre_is_sentence is True:
                            if previous + " " + current not in sen_start_dict:
                                sen_start_dict[previous + " " + current] = 1
                            else:
                                sen_start_dict[previous + " " + current] += 1
                        if pre_previous is not None and cur_is_sentence is True:
                            if pre_previous + " " + previous not in sen_end_dict:
                                sen_end_dict[pre_previous + " " + previous] = 1
                            else:
                                sen_end_dict[pre_previous + " " + previous] += 1
                    pre_previous = previous
                    previous = current
                    pre_is_sentence = cur_is_sentence
                    cur_is_sentence = False
                    # print "previous is:" + previous + "\n"
                    start = end
                    cur_is_sentence = False

def count_token_from_file_list(dir_path1, dir_path2, dir_path3, files1, files2, files3, token_dictionary, sen_start_dict, sen_end_dict, sen_flag):
        for file_path1 in files1:
            get_n_gram(dir_path1, file_path1, token_dictionary, sen_start_dict, sen_end_dict, sen_flag)
        for file_path2 in files2:
            get_n_gram(dir_path2, file_path2, token_dictionary, sen_start_dict, sen_end_dict, sen_flag)
        for file_path3 in files3:
            get_n_gram(dir_path3, file_path3, token_dictionary, sen_start_dict, sen_end_dict, sen_flag)



def count_total_number_dictionary(storage_dictionary):
    total_count = 0
    for dict_item in storage_dictionary:
        total_count += int(storage_dictionary[dict_item])
    return total_count


def get_two_gram(input_string, storage_dictionary1, storage_dictionary2,sen_start_dict, sen_end_dict, total_count):
    multi_ratio = 0
    dictionary_ratio = {}
    strs = input_string.split()
    multi_ratio += (np.log10(storage_dictionary1[strs[0]]) - np.log10(total_count))
    multi_ratio += (np.log10(sen_start_dict[strs[0] + " " + strs[1]]) - np.log10(storage_dictionary2[strs[0] + " " +\
                                                                                                     strs[1]]))
    multi_ratio += (np.log10(sen_end_dict[strs[len(strs) - 2] + " " + strs[len(strs) - 1]]) - \
                    np.log10(storage_dictionary2[strs[len(strs) - 2] + " " + strs[len(strs) - 1]]))
    for i in range(len(strs)-1):
        if str[i] in storage_dictionary1 and str[i] + " " + str[i + 1] in storage_dictionary2:
            dictionary_ratio[str[i] + " " + str[i + 1]] = np.log10(storage_dictionary2[str[i] + " " + str[i + 1]]) - \
                                                          np.log10(storage_dictionary1[str[i]])
            multi_ratio += dictionary_ratio[str[i] + " " + str[i + 1]]
    return multi_ratio, dictionary_ratio


def get_dictionary_from_txt_file(file_path):
    storage_dictionary = {}
    if not os.path.isdir(file_path):
        f = open(file_path)
        iter_f = iter(f)
        for line in iter_f:
            strs = line.split()
            storage_dictionary[strs[0]] = strs[1]
    return storage_dictionary


def get_dictionary_2_from_txt_file(file_path):
    storage_dictionary = {}
    if not os.path.isdir(file_path):
        f = open(file_path)
        iter_f = iter(f)
        for line in iter_f:
            strs = line.split()
            storage_dictionary[strs[0]+" "+strs[1]] = strs[2]
    return storage_dictionary


def get_bi_gram_from_file(file_path1, file_path2,file_path3, file_path4, input_string, total_count):
    storage_dictionary1 = get_dictionary_from_txt_file(file_path1)  # 1 gram
    storage_dictionary2 = get_dictionary_2_from_txt_file(file_path2)  # 2 gram
    sen_start_dict = get_dictionary_from_txt_file(file_path3)
    sen_end_dict = get_dictionary_from_txt_file(file_path4)
    multi_ratio, dictionary_ratio = get_two_gram(input_string, storage_dictionary1, storage_dictionary2, sen_start_dict, sen_end_dict, total_count)
    print "multi_ratio is :", multi_ratio, "\n"
    for dict_item in dictionary_ratio:
        print "key is:", dict_item, ";value is :", dictionary_ratio[dict_item], "\n"
    return multi_ratio, dictionary_ratio


def different_input_txt_file(input_name):
    multi_ratio, dictionary_ratio = get_bi_gram_from_file(file_path1, file_path2, file_path3,file_path4, input_name, total_count)
    with open('/Users/datamining/Desktop/3.txt', 'a') as f:
        str_write = str("%.6f" % multi_ratio)
        for dict_item in dictionary_ratio:
            str_write += ("  " + str(dict_item) + ":" + str("%.6f" % dictionary_ratio[dict_item]))
        str_write += "\n"
        f.write(str_write)


# different_input_txt_file(input1)
# different_input_txt_file(input2)
if __name__ == "__main__":
    path1 = "/Users/datamining/Desktop/CL_4th/test"
    path2 = "/Users/datamining/Desktop/CL_4th/train"
    path3 = "/Users/datamining/Desktop/CL_4th/valid"
    files1 = get_file_list(path1)
    files2 = get_file_list(path2)
    files3 = get_file_list(path3)
# token_dictionary = {}
# get_n_gram(path, files[0], token_dictionary)
    token_dictionary = {}
    count_token_from_file_list(path1, files1, token_dictionary)

    print len(token_dictionary)
    dict = sorted(token_dictionary.iteritems(), key=lambda d: d[1], reverse=True)
# dict = sortedDictValues1(token_dictionary)
    print dict[0:100]
# print json.dumps(token_dictionary, ensure_ascii=False, encoding='utf-8')

'''with open('/Users/datamining/Desktop/2.txt', 'w') as f:
    for ite in dict:
        f.write(ite[0]+'   '+str(ite[1])+'\n')'''
