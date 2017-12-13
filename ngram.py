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
    print(files_path)
    return files_path


'''
###files= os.listdir(path) #得到文件夹下的所有文件名称
s = []
for file in files: #遍历文件夹
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
          f = open(path+"/"+file); #打开文件
          iter_f = iter(f); #创建迭代器
          str = ""
          for line in iter_f: #遍历文件，一行行遍历，读取文本
              str = str + line
          s.append(str) #每个文件的文本存到list中
print(s) #打印结果  ###
'''


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


def count_token_from_file_list(dir_path1, dir_path2, dir_path3, files1, files2, files3, token_dictionary):
    for file_path1 in files1:
        get_n_gram(dir_path1, file_path1, token_dictionary)
    for file_path2 in files2:
        get_n_gram(dir_path2, file_path2, token_dictionary)
    for file_path3 in files3:
        get_n_gram(dir_path3, file_path3, token_dictionary)

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
    count_token_from_file_list(path1, path2, path3, files1, files2, files3, token_dictionary)
    print len(token_dictionary)
    dict = sorted(token_dictionary.iteritems(), key=lambda d: d[1], reverse=True)
    # dict = sortedDictValues1(token_dictionary)
    print dict[0:100]
    # print json.dumps(token_dictionary, ensure_ascii=False, encoding='utf-8')

    with open('/Users/datamining/Desktop/2.txt', 'w') as f:
        for ite in dict:
            f.write(ite[0]+'   '+str(ite[1])+'\n')

