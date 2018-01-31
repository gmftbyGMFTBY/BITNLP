#!/usr/bin/python3
# Author : Shaw
# Time   : 2017.1.23

'''
    MMR(Maximal Marginal Relevance) 算法对抽取的语句进行重新排序
    
    MMR := arg max [alpha * Sim(Di, Q) - (1 - alpha) * (max Sim(Di,Dj))]
    
    参数设定
        alpha := 0.7
'''

from operator import itemgetter
import re
import dataset

import jieba
import numpy as np

# 计算余弦相似度
def cos_similiar(vec_1, vec_2):
    # cos calculate the simliar about two vector
    # vec_1, vec_2 must be the ndarray of the numpy
    return np.sum(vec_1 * vec_2) / (np.sqrt(np.sum(vec_1 * vec_1)) * np.sqrt(np.sum(vec_2 * vec_2)))

def MMR(sentences, alpha, VSM):
    # 读取停用词
    stopwords = dataset.read_stopwords()
    
    # 生成词袋模型
    sent_array = []
    for sent in sentences:
        res_sent = jieba.lcut(sent)
        vec = [0] * VSM.shape[0]
        for index, word in enumerate(VSM):
            vec[index] = res_sent.count(word)
        sent_array.append(vec)
    sent_array = np.array(sent_array)
    
    # 计算句级相似度
    sim = np.zeros((VSM.shape[0], VSM.shape[0]))
    
    for i, vec1 in enumerate(sent_array):
        for j, vec2 in enumerate(sent_array):
            if i == j :
                continue
            else:
                sim[i, j] = cos_similiar(vec1, vec2)
                
    # MMR 算法
    n = round(0.6 * len(sentences))
    summary = []
    summary_index = []
    while n > 0 :
        mmr = {}
        for index, sent in enumerate(sentences):
            if sent not in summary:
                mmr[sent] = alpha * np.max(sim[index]) - (1 - alpha) * max_sim(sim, index, np.array(summary_index))
        selected = max(mmr.items(), key = itemgetter(1))[0]
        summary.append(selected)
        summary_index.append(get_summary_index(sentences, selected))
        n -= 1
    
    return summary

def get_summary_index(sentences, sent):
    # 获取当前的摘要列表
    for i, s in enumerate(sentences):
        if sent == s:
            return i

def max_sim(sim, index, summary_index):
    # 从相似度矩阵中选择最大相似度
    vec =  sim[index]
    max_ = - np.inf  
    if summary_index.shape[0] == 0:
        return 0
    else:
        return np.max(vec[summary_index])

if __name__ == "__main__":
    pass
