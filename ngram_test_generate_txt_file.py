# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



def get_file_list(file_path):
    files_path = os.listdir(file_path)
    return files_path


def get_n_gram(dir_path, file_path, token_dictionary, sen_start_dict, sen_end_dict, sen_flag):
    if not os.path.isdir(file_path):
        f = open(dir_path+"/"+file_path)
        iter_f = iter(f)
        for line in iter_f:
            line = line.decode('gb18030')
            # 加上这一步会简单很多啊，也是醉了
            # print line
            start = 0
            end = 0
            whitespace = 0
            pre_previous = None
            previous = None
            current = None
            pre_pre_is_sentence = False
            pre_is_sentence = True
            cur_is_sentence = False
            # print "len of line is :", len(line), "\n"
            for i in range(len(line)):
                if line[i] == '[':
                    start = i+1
                if line[i] == ' ':
                    whitespace += 1
                    if whitespace == 1:
                        start = i+2
                    if whitespace == 2:
                        whitespace = 0
                '''if i == len(line)-1 and line[i-2] not in sen_flag:
                    current = line[start:len(line)-2]
                    if current + " " + "<EOS>" not in sen_end_dict:
                        sen_end_dict[current + " " + "<EOS>"] = 1
                    else:
                        sen_end_dict[current + " " + "<EOS>"] += 1
                    print current + " " + "<EOS>"'''
                if line[i] == '/':
                    end = i
                if end > start:
                    # print line[i-1].decode('gb18030')
                    # temp = line[i-1: i].decode('gb18030')
                    if line[i-1] in sen_flag:
                        cur_is_sentence = True
                        # print line[i-1], i-1, "\n"
                    current = line[start: end]
                    # print "current is:" + current + "\n"
                    if previous is not None and current is not None:
                        if previous + " " + current not in token_dictionary:
                            token_dictionary[previous + " " + current] = 1
                        else:
                            token_dictionary[previous + " " + current] += 1
                        if pre_pre_is_sentence is True:
                            if "<BOS>" + " " + previous not in sen_start_dict:
                                sen_start_dict["<BOS>" + " " + previous] = 1
                            else:
                                sen_start_dict["<BOS>" + " " + previous] += 1
                        if previous is not None and cur_is_sentence is True and pre_previous is not None:
                            if previous + " " + "<EOS>" not in sen_end_dict:
                                sen_end_dict[previous + " " + "<EOS>"] = 1
                            else:
                                sen_end_dict[previous + " " + "<EOS>"] += 1
                    pre_previous = previous
                    previous = current
                    pre_pre_is_sentence = pre_is_sentence
                    pre_is_sentence = cur_is_sentence
                    # print "previous is:" + previous + "\n"
                    start = end
                    cur_is_sentence = False


def count_token_from_file_list(dir_path1, dir_path2, dir_path3, files1, files2, files3, token_dictionary,
                               sen_start_dict, sen_end_dict, sen_flag):
    for file_path1 in files1:
        get_n_gram(dir_path1, file_path1, token_dictionary, sen_start_dict, sen_end_dict, sen_flag)
    for file_path2 in files2:
        get_n_gram(dir_path2, file_path2, token_dictionary, sen_start_dict, sen_end_dict, sen_flag)
    for file_path3 in files3:
        get_n_gram(dir_path3, file_path3, token_dictionary, sen_start_dict, sen_end_dict, sen_flag)


if __name__ == '__main__':
    path1 = "/Users/datamining/Desktop/CL_4th/test"
    path2 = "/Users/datamining/Desktop/CL_4th/train"
    path3 = "/Users/datamining/Desktop/CL_4th/valid"
    files1 = get_file_list(path1)
    files2 = get_file_list(path2)
    files3 = get_file_list(path3)

# token_dictionary = {}
# get_n_gram(path, files[0], token_dictionary)
    token_dictionary = {}
    sen_start_dict = {}
    sen_end_dict = {}
    sen_flag = "。？！：；".decode('utf-8')
    for elem in sen_flag:
        print elem

# count_token_from_file_list(path1, path2, path3, files1, files2, files3, token_dictionary, sen_start_dict, sen_end_dict, sen_flag)
    for file_pa in files3:
        get_n_gram(path3, file_pa, token_dictionary, sen_start_dict, sen_end_dict, sen_flag)
    for file_pa in files2:
        get_n_gram(path2, file_pa, token_dictionary, sen_start_dict, sen_end_dict, sen_flag)
    print "len of token_dictionary is:", len(token_dictionary), "\n"
    print "len of sen_start_dict is:", len(sen_start_dict), "\n"
    print "len of sen_end_dict is:", len(sen_end_dict), "\n"

# print sen_start_dict
    print json.dumps(sen_start_dict, ensure_ascii=False, encoding='utf-8')
# print sen_end_dict
    print json.dumps(sen_end_dict, ensure_ascii=False, encoding='utf-8')

    sen_start_count = 0
    for ite in sen_start_dict:
        sen_start_count += sen_start_dict[ite]
    sen_end_count = 0
    for ite in sen_end_dict:
        sen_end_count += sen_end_dict[ite]

    print "sen_start_count is:", sen_start_count, "\n"
    print "sen_end_count is:", sen_end_count, "\n"
    '''dict = sorted(token_dictionary.iteritems(), key=lambda d: d[1], reverse=True)
    # dict = sortedDictValues1(token_dictionary)
    print dict[0:100]
    print json.dumps(token_dictionary, ensure_ascii=False, encoding='utf-8')'''
    sen_start = sorted(sen_start_dict.iteritems(), key=lambda d: d[1], reverse=True)
    sen_end = sorted(sen_end_dict.iteritems(), key=lambda d: d[1], reverse=True)
    print sen_start[0:100]
    with open('/Users/datamining/Desktop/11.txt', 'w') as f:
        for ite in sen_start:
            f.write(ite[0].decode('utf-8') + '   '+str(ite[1])+'\n')
        # print ite, str(sen_start_dict[ite])
    with open('/Users/datamining/Desktop/12.txt', 'w') as f:
        for ite in sen_end:
            f.write(ite[0].decode('utf-8') + '   '+str(ite[1])+'\n')
        # print ite[0], str(ite[1])

    temp = "<BOS>" + " " + "扶贫"
    temp = temp.decode('utf-8')
    print temp, ":", sen_start_dict[temp]

    temp2 = "成绩" + " " + "<EOS>"
    temp2 = temp2.decode('utf-8')
    print temp2, ":", sen_end_dict[temp2]
