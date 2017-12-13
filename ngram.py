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


def get_n_gram(dir_path, file_path, token_dictionary):
    if not os.path.isdir(file_path):
        f = open(dir_path+"/"+file_path)
        iter_f = iter(f)
        for line in iter_f:
            # print line.decode('gb18030')
            start = 0
            end = 0
            whitespace = 0
            previous = None
            current = None
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
                    current = line[start: end].decode('gb18030')
                    # print "current is:" + current + "\n"
                    if previous is not None and current is not None:
                        if previous + " " + current not in token_dictionary:
                            token_dictionary[previous + " " + current] = 1
                        else:
                            token_dictionary[previous + " " + current] += 1
                    previous = current
                    # print "previous is:" + previous + "\n"
                    start = end


def count_token_from_file_list(dir_path, files, token_dictionary):
    for file_path in files:
        get_n_gram(dir_path, file_path, token_dictionary)


path = "/Users/datamining/Desktop/CL_4th"
files = get_file_list(path)

# token_dictionary = {}
# get_n_gram(path, files[0], token_dictionary)
token_dictionary = {}
count_token_from_file_list(path, files, token_dictionary)

print len(token_dictionary)
dict = sorted(token_dictionary.iteritems(), key=lambda d: d[1], reverse=True)
# dict = sortedDictValues1(token_dictionary)
print dict[0:100]
# print json.dumps(token_dictionary, ensure_ascii=False, encoding='utf-8')

with open('/Users/datamining/Desktop/2.txt', 'w') as f:
    for ite in dict:
        f.write(ite[0]+'   '+str(ite[1])+'\n')

