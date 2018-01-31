#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.1.23

'''
    该脚本尝试从搜狗实验室提供的新闻数据中抽取出主要的内容
        ** 搜狗实验室 **
    首先项搜狗实验室表达感谢
'''

from bs4 import BeautifulSoup
import random

def read_sogou(count = None):
    # count = None 返回整段语料库
    with open('data/news_result.txt') as f:
        raw = f.read()
        raw = raw.replace('\ue40c', '\n')
        raw = raw.replace('\u3000', ' ')
    soup = BeautifulSoup(raw, 'lxml')
    docs = soup.find_all(name = 'doc')
    file = []
    for index, doc in enumerate(docs):
        if doc.content.string is None:
            continue
        file.append(doc.content.string)
    if count is None:
        # random.shuffle(file)
        return file
    else:
        # 随机选择一个文件
        index = random.randint(0,len(file) - 1)
        return file[index], index

def read_stopwords():
    # 读取停用词
    with open('data/stopwords') as f:
        raw = f.read()
    raw = raw.split('\n')
    return raw
    
def read_test():
    # 测试阅读模块, 该文本来自于语料库的139号文本
    doc = '腾讯科技讯（刘亚澜）10月22日消息，前优酷土豆技术副总裁黄冬已于日前正式加盟芒果TV，出任CTO一职。资料显示，黄冬历任土豆网技术副总裁、优酷土豆集团产品技术副总裁等职务，曾主持设计、运营过优酷土豆多个大型高容量产品和系统。此番加入芒果TV或与芒果TV计划自主研发智能硬件OS有关。今年3月，芒果TV对外公布其全平台日均独立用户突破3000万，日均VV突破1亿，但挥之不去的是业内对其技术能力能否匹配发展速度的质疑，亟须招揽技术人才提升整体技术能力。芒果TV是国内互联网电视七大牌照方之一，之前采取的是“封闭模式”与硬件厂商预装合作，而现在是“开放下载”+“厂商预装”。黄冬在加盟土豆网之前曾是国内FreeBSD（开源OS）社区发起者之一，是研究并使用开源OS的技术专家，离开优酷土豆集团后其加盟果壳电子，涉足智能硬件行业，将开源OS与硬件结合，创办魔豆智能路由器。未来黄冬可能会整合其在开源OS、智能硬件上的经验，结合芒果的牌照及资源优势，在智能硬件或OS领域发力。公开信息显示，芒果TV在今年6月对外宣布完成A轮5亿人民币融资，估值70亿。据芒果TV控股方芒果传媒的消息人士透露，芒果TV即将启动B轮融资。'
    return doc, 139
    
if __name__ == "__main__":
    # read the file from sogou
    # docs, index = read_sogou(1)
    # print(docs, index)
    print(read_stopwords())
    
