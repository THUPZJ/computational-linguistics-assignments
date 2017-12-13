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
    # print(files_path)
    return files_path


def count_token_from_txt_file(dir_path, file_path, token_dictionary):
    if not os.path.isdir(file_path):
        f = open(dir_path+"/"+file_path)
        iter_f = iter(f)
        for line in iter_f:
            # print line.decode('gb18030')
            start = 0
            end = 0
            whitespace = 0
            # is_sentence = True
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
                    if line[start:end].decode('gb18030') not in token_dictionary:
                        token_dictionary[line[start:end].decode('gb18030')] = 1
                    else:
                        token_dictionary[line[start:end].decode('gb18030')] += 1
                    start = end


def count_token_from_file_list(dir_path1, dir_path2, dir_path3, files1, files2, files3, token_dictionary):
    for file_path1 in files1:
        count_token_from_txt_file(dir_path1, file_path1, token_dictionary)
    for file_path2 in files2:
        count_token_from_txt_file(dir_path2, file_path2, token_dictionary)
    for file_path3 in files3:
        count_token_from_txt_file(dir_path3, file_path3, token_dictionary)


'''def sorted_dict_values1(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]'''


'''dict = {'Title': '这是标题'}
print json.dumps(dict, ensure_ascii=False, encoding='utf-8')'''


'''
path1 = "/Users/datamining/Desktop/CL_4th/test"
path2 = "/Users/datamining/Desktop/CL_4th/train"
path3 = "/Users/datamining/Desktop/CL_4th/valid"
files1 = get_file_list(path1)
files2 = get_file_list(path2)
files3 = get_file_list(path3)
token_dictionary = {}
count_token_from_file_list(path1, path2, path3, files1, files2, files3, token_dictionary)


#count_token_from_txtfile(path, files[0], token_dictionary)'''
'''for token, number in token_dictionary:
    print token.decode("unicode-escape"), ":", number, "\n"'''
'''
#print token_dictionary
print len(token_dictionary)
dict = sorted(token_dictionary.iteritems(), key=lambda d: d[1], reverse=True)

print dict[0:100]
#print json.dumps(token_dictionary, ensure_ascii=False, encoding='utf-8')

with open('/Users/datamining/Desktop/1.txt', 'w') as f:
    for ite in dict:
        f.write(ite[0]+'   '+str(ite[1])+'\n')
    #f.write('one\n')
    #f.write('two')

frequency_list = []
for dict_item in dict:
    frequency_list.append(dict_item[1])
#print frequency_list
rank_frequency_list = []
for i in range(len(frequency_list)):
    rank_frequency_list.append(i+1)


plt.plot(np.log10(rank_frequency_list), np.log10(frequency_list))
plt.xlabel("log rank")
plt.ylabel("log frequency")
plt.show()'''
'''s = []
for File in files:   #遍历文件夹
    print File.title()''' # 打印结果'''
'''if not os.path.isdir(File):   #判断是否是文件夹，不是文件夹才打开
          f = open(path+"/"+File);   #打开文件
          iter_f = iter(f);   #创建迭代器
          str = ""
          for line in iter_f:   #遍历文件，一行行遍历，读取文本
              str = str + line
          s.append(str)   #每个文件的文本存到list中'''
#print File.title()   #打印结果