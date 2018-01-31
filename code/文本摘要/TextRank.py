#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.1.23

'''
    TextRank 算法, 使用 TF-IDF 更新关键词，使用 MMR 对抽取句子重排
    构成摘要
'''

import TFIDF
import dataset
from collections import defaultdict
from operator import itemgetter
import numpy as np
import analyser
import MMR

from operator import itemgetter

# ---- 相似度计算工具，从论文中获取的公式 ---- #
def textrank_similiar(vec_1, vec_2):
    v1 = set(vec_1)
    v2 = set(vec_2)
    share = v1 & v2
    return len(share) / (np.log(len(v1) + np.log(len(v2))))

# ---- similiar utils end ---- #

class Graph:
    def __init__(self, d, iterations):
        # TextRank算法中的 `逃逸权重` 设定在0.85
        self.d     = d
        self.graph = defaultdict(list)    # 图
        self.dimension = 1                # 节点维度
        self.iter = iterations            # 迭代次数
        self.WS   = None                  # 节点
    
    def add_edge(self, s, e, weight):
        # 图加边
        # 一次加两条有权无向边
        self.graph[s].append((s, e, weight))
        self.graph[e].append((e, s, weight))
        
    def rank(self):
        # 初始化迭代次数
        self.dimension = len(self.graph)
        if self.dimension == 0 : self.dimension = 1
        
        WS     = defaultdict(float)    # 计算初始节点值
        outsum = defaultdict(float)    # 每个节点的出边和入边权重和
        
                            
        init_ws = 1 / self.dimension
        # 初始化节点权值和总权重
        for node, out in self.graph.items():
            WS[node] = init_ws
            outsum[node] = sum([edge[2] for edge in out])
        
        # 迭代 TextRank
        for i in range(self.iter):
            # iter each node
            for node in self.graph.keys():
                s = 0
                for edge in sorted(self.graph[node]):
                    s += edge[2] * WS[edge[1]] / outsum[edge[1]]
                WS[node] = (1 - self.d) + self.d * s
                
        # 归一化
        if len(WS.keys()) == 0:
            return False
        
        min_ = min(WS.values())
        max_ = max(WS.values())
        
        for node, W in WS.items():
            WS[node] = (W - min_) / (max_ - min_)
            
        # 结果保存
        self.WS = WS

class TextRank:
    '''
    使用TextRank实例抽取关键词和关键句
    '''
    def __init__(self, span, d, iterations, index):
        self.kspan = span    # 共现窗口的长度
        self.d = d
        self.iteration = iterations
        
        # ---- TF-IDF 初始化 ---- #
        docs = dataset.read_sogou()
        for i, doc in enumerate(docs):
            docs[i] = TFIDF.cut_by_words(doc) 
        data, self.VSM = TFIDF.create_VSM(docs)
        print("Create VSM Over !")
        # 生成 IDF 
        self.idf = TFIDF.IDF(data, self.VSM)
        self.tfidf = TFIDF.TF_IDF(data[index], self.VSM, self.idf)
        self.keywords_doc = TFIDF.extract_keywords_tfidf(self.tfidf, self.VSM)
        
        print("Got the keywors from the docs !")
        
    def textrank_words(self, sentence, size):
        '''
            使用TextRank算法抽取关键字
        '''
        graph = Graph(self.d, self.iteration)
        
        # the TextRank Algorithm and return `size` keywords of the sentence
        words = TFIDF.cut_by_words(sentence)
        # Create the graph for the TextRank
        
        # clean with the stopwords and symbol in the sentence
        stopwords_set = TFIDF.get_stopwords()
        edge_weight = defaultdict(int)    # count the weight of the edge 
        for index_i, word in enumerate(words):
            if word not in stopwords_set:
                for index in range(index_i + 1, index_i + self.kspan):
                    if index >= len(words):
                        # end this loop
                        break
                    if words[index] in stopwords_set:
                        # do not care about the stopwords
                        continue
                    # add the edge, defaultdict default that is 0
                    edge_weight[(word, words[index])] += 1
        
        # create the graph of the word
        for key, value in edge_weight.items():
            graph.add_edge(key[0], key[1], value)

        res = graph.rank()
        if res == False:
            return False
        
        result = sorted(graph.WS.items(), key = itemgetter(1), reverse = True)
        result = join_result(result, sentence)
        result = sorted(graph.WS.items(), key = itemgetter(1), reverse = True)
        
        if size > len(result):
            print("Overload !")
            size = len(result)
        
        return result[:size]
    
    def textrank_sentence(self, doc, threshold):
        '''
        使用 TextRank 算法抽取关键句，使用论文中提供的相似度计算公式，详见实验报告
        抽取 `size` 个句子作为下一次喂给 MMR 的输入
        '''
        
        # create the undirect graph for the textrank sentences
        graphh = Graph(self.d, self.iteration)
        
        sentences = TFIDF.cut_by_sentence(doc)
        
        # change the size_word dynamicly
        if len(sentences) < 9 :
            size_word = 2
        else:
            # maybe 6
            size_word = 5
        
        if len(sentences) <= 4 :
            print("The content is too short, do not need to summary !")
            return sentences
        
        # size may need to large as 0.6
        size = round(len(sentences) * 0.3)
        if size == 0 :
            size = min(1, len(sentences))
        # use TextRank to get the keywords from the sentence
        
        # Get Keywords, need to fix
        # get the data
        sentences_array = []
        for sent in sentences:
            result = self.textrank_words(sent, size_word)
            
            if result == False:
                # do not find the keywords with the TextRank
                result = []
            
            # TFIDF 补充关键字,并考虑合并关键词组
            result = append_keywords(sent, result, self.keywords_doc)
            # result = join_result(result, sent)
            # add the keywords with the TFIDF
            
            if result == False:
                words = []
            else:
                words  = list(map(lambda x : x[0], result))
            sentences_array.append(words)
        
        # Get Keywords Over, need to finish fix operator
        
        # 初始化 TextRank 图
        for i, sent1 in enumerate(sentences_array):
            for j, sent2 in enumerate(sentences_array):
                if i == j or len(sent1) == 0 or len(sent2) == 0: 
                    continue
                weights = textrank_similiar(np.array(sent1), np.array(sent2))
                if weights > threshold:
                    # similiar
                    graphh.add_edge(i, j, weights)
        
        # 图排序开始
        graphh.rank()
        result = graphh.WS
        
        if result is None:
            print("Error, because of the high threshold !")
            return False
        
        result = sorted(result.items(), key = itemgetter(1), reverse = True)
        
        if size > len(result):
            print("Overload !")
            size = len(result)
        result = result[:size]
        
        # 句子抽取
        result_sent = []
        for i, j in result:
            result_sent.append(sentences[i])
        
        return result_sent

def append_keywords(sent, result, keywords_doc):
    # 使用 TF-IDF 返回补充后的关键字列表
    result = [item[0] for item in result]
    cha = []
    for word, weight in keywords_doc:
        try:
            res = sent.index(word)
            if word in result:
                continue
            else:
                cha.append((word, weight))
        except:
            continue
    result = set(result)
    size = 2
    if len(cha) < size:
        size = len(cha)
    cha    = sorted(cha, key = itemgetter(1), reverse = True)[:size]
    cha    = set([item[0] for item in cha])
    result |= cha
    return list(result)
    
def sort_merge_sentence(doc, result):
    # 对抽取的句子在文本级按照出现的先后顺序做排序，保证摘要的可读性
    
    result = [(sent, doc.index(sent)) for sent in result]
    result = sorted(result, key = itemgetter(1))
    
    result = [sent[0] for sent in result]
    
    s = '。'.join(result)
    s += '。'    # the EOF ending.
    return s
    
def summary(doc, index = None):
    # 摘要抽取函数
    tr = TextRank(5, 0.85, 10, index)
    # the threshold may cause the error, be careful !!!
    result = tr.textrank_sentence(doc, 0.2)
    if result == False:
        return
    
    # ---- MMR 过滤重排 ---- #
    # 参数 : alpha
    #   1. 高 alpha : 高精准度，低多样性
    #   2. 低 alpha : 高多样性，低精准度
    # result = MMR.MMR(result, 0.4, tr.VSM)   
    
    # ---- MMR filter resort ---- #
    
    return sort_merge_sentence(doc, result)
    

def join_result(result, sentence):
    # 如果关键字是连续的，可以考虑合并成关键词组
    for index, item in enumerate(result):
        try :
            i = sentence.index(item[0])
            result[index] = (i, i + len(item[0]), item[0], item[1])
        except:
            print(sentence, item)
            
    result = sorted(result, key = itemgetter(0))
    point = 0
    n_r = []
    while point < len(result) - 1:
        ele   = []
        while result[point][1] == result[point + 1][0]:
            ele.append(point)
            point += 1
            if point >= len(result) - 1:
                break
        ele.append(point)
        n_r.append(ele)
        point += 1
    # very stupid
    new_result = []
    for i in n_r:
        s = ''
        weights = 0
        for j in i:
            s += result[j][2]
            weights += result[j][3]
        new_result.append((s, weights))
    return new_result

if __name__ == "__main__":
    # test for textrank_words
    
    # tr = TextRank(5, 0.85, 10)
    # result = tr.textrank_words("我是一名共产主义的忠实的拥护者，是一个合格的共产党员，忠实的维护党的利益", 10)
    # print(result)
    
    # ---- keywords from TFIDF ---- #
    
    # ---- test for textrank_sentences ---- #
    # doc = '腾讯科技讯（刘亚澜）10月22日消息，前优酷土豆技术副总裁黄冬已于日前正式加盟芒果TV，出任CTO一职。资料显示，黄冬历任土豆网技术副总裁、优酷土豆集团产品技术副总裁等职务，曾主持设计、运营过优酷土豆多个大型高容量产品和系统。此番加入芒果TV或与芒果TV计划自主研发智能硬件OS有关。今年3月，芒果TV对外公布其全平台日均独立用户突破3000万，日均VV突破1亿，但挥之不去的是业内对其技术能力能否匹配发展速度的质疑，亟须招揽技术人才提升整体技术能力。芒果TV是国内互联网电视七大牌照方之一，之前采取的是“封闭模式”与硬件厂商预装合作，而现在是“开放下载”+“厂商预装”。黄冬在加盟土豆网之前曾是国内FreeBSD（开源OS）社区发起者之一，是研究并使用开源OS的技术专家，离开优酷土豆集团后其加盟果壳电子，涉足智能硬件行业，将开源OS与硬件结合，创办魔豆智能路由器。未来黄冬可能会整合其在开源OS、智能硬件上的经验，结合芒果的牌照及资源优势，在智能硬件或OS领域发力。公开信息显示，芒果TV在今年6月对外宣布完成A轮5亿人民币融资，估值70亿。据芒果TV控股方芒果传媒的消息人士透露，芒果TV即将启动B轮融资。'
    print("begin " + '-' * 20)
    doc, index = dataset.read_sogou(1)
    #index = 139
    summary = summary(doc, index)
    print("summary : -----")
    print(summary)
    print("origin : -----")
    print(doc)
