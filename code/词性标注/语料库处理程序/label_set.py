'''
Created on 2017年12月27日

@author: KanSunny
'''
'''
功能：用于检测语料库中用到的标注集
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
            string = string.split('/')
            with open('F:/大三上课件/NLP/lable_set.txt', 'a') as f:
                for str in string:
                    lable = ''
                    for i in str:
                        if (i[0] >= 'a' and i[0] <= 'z') or (i[0] >= 'A' and i[0] <= 'Z'):
                            lable += i[0]
                        else:
                            break
                    if len(lable):
                        if lable not in lable_set:
                            lable_set.append(lable)
                            f.write(lable+' ')
                            if lable not in lable_rule:
                                with open('F:/大三上课件/NLP/lable_error.txt', 'a') as fp:
                                    fp.write(lable + ' ')