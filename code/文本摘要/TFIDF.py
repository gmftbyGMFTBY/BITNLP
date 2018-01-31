#!/usr/bin/python3
# Author : KanSunny
# Time   : 2017.1.23

'''
    使用 TF-IDF 算法计算语料库中文本的关键字，作为对 TextRank 算法对关键字方面提取的补充
'''

import dataset
import jieba    # 我们这里测试中采用jieba，方便迅速，实际中，我们乣替换成自然语言处理大作业一中的自己编写的分词软件，这里仅仅是为了速度考虑，希望老师可以理解
import numpy as np
from operator import itemgetter
import re

def get_stopwords():
    # 抽取停用词
    with open('data/stopwords') as f:
        raw = f.read()
    stopwords = set(raw.split())
    # 添加' ', '\n' 到停用词列表
    stopwords |= set([' ', '\n'])
    return stopwords

def create_VSM(cut_docs):
    # 创建词袋模型
    # 加载停用词
    # return VSM in the `set`
    stopwords = get_stopwords()
    VSM = set()
    for doc in cut_docs:
        c_doc = set(doc) - set(stopwords)
        VSM |= c_doc
    
    VSM = np.array(list(VSM))    # 生成向量模型控件矩阵
    print("create the VSM Over !")
    data = []
    for doc in cut_docs:
        row = []
        for word in VSM:
            row.append(doc.count(word) * 1.0)
        data.append(row)
    print("create the array Over !")
    return np.array(data), VSM

def cut_by_words(doc):
    # 分词操作，为了速度考虑，我们这里使用jieba库，实际中我们会使用自己编写的分词软件
    return jieba.lcut(doc)

def cut_by_sentence(doc):
    # 句级切分
    # 切分的句子数目不够，使用粒度更低的切分方式，保证切分的句子的数目
    sents = re.split(u'[。！？；\\n]', doc)
    sent = []
    for i in sents:
        if i != '':
            sent.append(i)
    if len(sent) < 9:
        # too short, try to split more 
        sents = re.split(u'[，。！？；\\n]', doc)
    sent = []
    for i in sents:
        if i != '':
            sent.append(i)
    return sent

def IDF(data, VSM):
    # 计算IDF矩阵
    # testing, no problem
    doc_num = data.shape[1]
    idf = np.log(doc_num / (np.count_nonzero(data, axis = 0) + 1))
    return idf        

def TF_IDF(data_once, VSM, idf):
    # 计算 TF-IDF
    # 一次只计算一个文本的 TF-IDF
    # 计算结果不错，和sklearn中自带的计算 TF-IDF 的算法的计算结果基本保持一致
    word_sum = np.sum(data_once)
    tf = data_once / word_sum
    tf_idf = tf * idf
    return tf_idf

def extract_keywords_tfidf(tfidf, VSM, size = None):
    # 利用计算的 TF-IDF 矩阵抽取关键词
    # size = None, 返回所有的抽取关键词
    # 否则只返回 `size` 个关键字，top(size)
    index = np.nonzero(tfidf)[0]
    keywords = {}
    for i in index:
        keywords[VSM[i]] = tfidf[i]
    keywords = sorted(keywords.items(), key = itemgetter(1), reverse = True)
    if size is None:
        return keywords
    else:
        if size > len(keywords):
            print("Overload !")
            size = len(keywords)
        return keywords[:size]
    
if __name__ == "__main__":
    docs = dataset.read_sogou()
    for index, doc in enumerate(docs):
        docs[index] = cut_by_words(doc) 
    
    data, VSM = create_VSM(docs)
    idf = IDF(data, VSM)
    print("IDF Over !")
    print(docs[0])
    tfidf = TF_IDF(data[0], VSM, idf)
    kw = extract_keywords_tfidf(tfidf, VSM)
    print(kw)
    
    # test with the sklearn 
    from sklearn.feature_extraction.text import TfidfTransformer
    p = TfidfTransformer()
    tfidf2 = p.fit_transform(data)[0].toarray()
    tfidf2 = tfidf2[np.nonzero(tfidf2)]
    
    # compare the tfidf result with sklearn
    print('Mine :')
    print(tfidf[np.nonzero(tfidf)])
    print("Sklearn :")
    print(tfidf2)
    
    
