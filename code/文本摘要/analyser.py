#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.1.23

'''
    This script try to use the Edmundson Algorithm to analyse the result of the summary
'''

import TFIDF

def Edmundson(result, answer):
    # result 机器摘要
    # answer 参考摘要
    r_s = set(TFIDF.cut_by_sentence(result))
    r_a = set(TFIDF.cut_by_sentence(answer))
    share = r_s & r_a
    return len(share) / len(r_a)

if __name__ == "__main__":
    answer = '一度疯狂的ＩＰＯ申报脚步于近日呈大幅放缓趋势。上周主板无新增初审企业。山东龙大肉食品、福建安溪铁观音集团、广东台城制药和海洋王照明科技４家拟主板企业于上周进行预披露。 创业板 方面，南京宝色、丹东欣泰电气和深圳市凯立德科技也已公布招股说明书。'
    summary = '３０６家（包括１３家中止审查企业）。上周主板无新增初审企业。ＩＰＯ申报企业基本信息显示。仅有３家拟上市企业进入候审队伍。山东龙大肉食品、福建安溪铁观音集团、广东台城制药和海洋王照明科技４家拟主板企业于上周进行预披露。南京宝色、丹东欣泰电气和深圳市凯立德科技也已公布招股说明书。'
    print(Edmundson(summary, answer))
