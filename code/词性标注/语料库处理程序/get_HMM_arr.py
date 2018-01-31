'''
Created on 2018年1月13日

@author: KanSunny

功能：统计训练集中每个词的每个可能词性概率，本次标记集大小为125
'''

import os
import re
import json

if __name__ == '__main__':
    # 词 及 词性概率
    word_pos = {}
    # 标注集
    lables = []
    # 所有出现的词
    word = []
    # 先验概率数组
    arr = {}
    # 出现次数
    appear_num = [0 for n in range(125)]
    test = 0

    # 初始化先验矩阵
    for i in range(125):
        zero = [0 for n in range(126)]
        arr[i] = zero
        
    with open('F:/大三上课件/NLP/lable_rule.txt', 'r', encoding = 'utf8') as fp:
        string = []
        string = fp.read()
        lables = string.split()
        
    with open('F:/大三上课件/NLP/corpus.txt', 'r', encoding='utf8') as fp:
        string = []
        string  = fp.read()
        print('the len of this test file is', len(string))
        word_and_lable = []
        word_and_lable = string.split()
        print('the num of word', len(word_and_lable))
        fore_num = 125
        for temp in word_and_lable:
            test += 1
            if test%1000 == 0:
                print(test)
            temp = temp.split('/')
            if len(temp) != 2:
                continue
            # 未记录词登记
            if temp[0] not in word:
                zero = [0 for n in range(125)]
                word.append(temp[0])
                word_pos[temp[0]] = zero
            # 该词性出现次数登记    
            for i in range(len(lables)):
                if lables[i] == temp[1]:
                    arr[i][fore_num] += 1
                    fore_num = i
                    word_pos[temp[0]][i] += 1
                    appear_num[i] += 1
                    break
    with open('F:/大三上课件/NLP/word_sign.json', 'a', encoding = 'utf8') as fp:
        json.dump(word_pos, fp, ensure_ascii = False)
        fp.write('\n')
    with open('F:/大三上课件/NLP/fore_arr.json', 'a', encoding = 'utf8') as fp:
        json.dump(arr, fp, ensure_ascii = False)
        fp.write('\n')
    with open('F:/大三上课件/NLP/appear_times.json', 'a', encoding = 'utf8') as fp:
        json.dump(appear_num, fp, ensure_ascii = False)
        fp.write('\n')
    print('finish')