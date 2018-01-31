'''
Created on 2018年1月13日

@author: KanSunny

功能：用于将语料库融合到一个文件中
'''

import os

if __name__ == '__main__':
    
    lable_set = []
    txtnum = 0
    lable_rule = []
    root = 'F:/大三上课件/NLP/北大2014语料库'
    with open('F:/大三上课件/NLP/lable_rule.txt', 'r', encoding='utf8') as f:
        lable_rule = f.read()
        lable_rule = lable_rule.split()
    allfile = os.listdir(root)
    for filename in allfile:
        file_loc = root + '/' + filename
        alltxt = os.listdir(file_loc)
        for txtname in alltxt:
            txt_loc = file_loc + '/' + txtname
            string = []
            with open(txt_loc, 'r', encoding='utf8') as f:
                txtnum += 1
                print(txtnum)
                string = f.read()
                with open('F:/大三上课件/NLP/corpus.txt', 'a', encoding='utf8') as fp:
                    #print(string)
                    string = string.split('\n')
                    #print(string[0])
                    fp.write(string[0])