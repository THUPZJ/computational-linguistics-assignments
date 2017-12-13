# -*- coding:utf-8 -*-
import numpy as np
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




def count_total_number_dictionary(storage_dictionary):
    total_count = 0
    for dict_item in storage_dictionary:
        total_count += int(storage_dictionary[dict_item])
    return total_count


def get_two_gram(input_string, storage_dictionary1, storage_dictionary2, total_count):
    multi_ratio = 0
    dictionary_ratio = {}
    strs = input_string.split()
    # print 'storage_dictionary1[strs[0]] is:', storage_dictionary1[strs[0]], "\n"
    print "key is:", strs[0], ";value is:", np.log10(int(storage_dictionary1[strs[0]])) - np.log10(total_count)
    multi_ratio += (np.log10(int(storage_dictionary1[strs[0]])) - np.log10(total_count))
    for i in range(len(strs)-1):
        temp = strs[i] + " " + strs[i + 1]
        if strs[i] in storage_dictionary1 and temp in storage_dictionary2:
            dictionary_ratio[temp] = np.log10(int(storage_dictionary2[temp])) - np.log10(int(storage_dictionary1[strs[i]]))
            multi_ratio += dictionary_ratio[temp]
    return multi_ratio, dictionary_ratio


def get_one_gram(input_string, storage_dictionary1, total_count):
    multi_ratio = 0
    dictionary_ratio = {}
    strs = input_string.split()
    # multi_ratio += (np.log10(int(storage_dictionary1[strs[0]])) - np.log10(total_count))
    for i in range(len(strs)):
        if strs[i] in storage_dictionary1:
            dictionary_ratio[strs[i]] = np.log10(int(storage_dictionary1[strs[i]])) - np.log10(total_count)
            multi_ratio += dictionary_ratio[strs[i]]
    return multi_ratio, dictionary_ratio


def get_dictionary_from_txt_file(file_path):
    storage_dictionary = {}
    if not os.path.isdir(file_path):
        f = open(file_path)
        iter_f = iter(f)
        for line in iter_f:
            strs = line.split()
            storage_dictionary[strs[0]] = int(strs[1])
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


def get_bi_gram_from_file(file_path1, file_path2, input_string):
    storage_dictionary1 = get_dictionary_from_txt_file(file_path1)  # 1 gram
    storage_dictionary2 = get_dictionary_2_from_txt_file(file_path2)  # 2 gram
    total_count = count_total_number_dictionary(storage_dictionary1)
    multi_ratio, dictionary_ratio = get_two_gram(input_string, storage_dictionary1, storage_dictionary2, total_count)
    print "multi_ratio is :", multi_ratio, "\n"
    for dict_item in dictionary_ratio:
        print "key is:", dict_item, ";value is :", dictionary_ratio[dict_item], "\n"
    return multi_ratio, dictionary_ratio


def get_one_gram_from_file(file_path1, input_string):
    storage_dictionary1 = get_dictionary_from_txt_file(file_path1)
    total_count = count_total_number_dictionary(storage_dictionary1)
    multi_ratio, dictionary_ratio = get_one_gram(input_string, storage_dictionary1, total_count)
    print "multi_ratio is :", multi_ratio, "\n"
    for dict_item in dictionary_ratio:
        print "key is:", dict_item, ";value is :", dictionary_ratio[dict_item], "\n"
    return multi_ratio, dictionary_ratio


def different_input_txt_file(input_name):
    # total_count = count_total_number_dictionary()
    multi_ratio, dictionary_ratio = get_bi_gram_from_file(file_path1, file_path2, input_name)
    with open('/Users/datamining/Desktop/3.txt', 'a') as f:
        str_write = str("%.6f" % multi_ratio)
        for dict_item in dictionary_ratio:
            str_write += ("  " + str(dict_item) + ":" + str("%.6f" % dictionary_ratio[dict_item]))
        str_write += "\n"
        f.write(str_write)


def same_input_txt_file(input_name):
    multi_ratio, dictionary_ratio = get_one_gram_from_file(file_path1,input_name)
    with open('/Users/datamining/Desktop/3.txt', 'a') as f:
        str_write = str("%.6f" % multi_ratio)
        for dict_item in dictionary_ratio:
            str_write += ("  " + str(dict_item) + ":" + str("%.6f" % dictionary_ratio[dict_item]))
        str_write += "\n"
        f.write(str_write)


if __name__ == "__main__":
    file_path1 = '/Users/datamining/Desktop/1.txt'
    file_path2 = '/Users/datamining/Desktop/2.txt'

    input1 = "扶贫 开发 工作 取得 很 大 成绩"
    input2 = "扶贫 开发 工作 得到 很 大 成绩"
    different_input_txt_file(input1)
# different_input_txt_file(input2)
# same_input_txt_file(input2)
