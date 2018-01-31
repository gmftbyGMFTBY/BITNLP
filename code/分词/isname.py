import sys
def cal_family_name(name_path,path):

    word_count = dict()
    frq = 0
    f1 = open(path,'r',encoding='utf-8')
    line = f1.readline()
    while line:
        for i in line.split(' '):
            j= 0
            while j < i.__len__():
                if i[j] in word_count:
                    word_count[i[j]] +=1
                else:
                    word_count[i[j]] =1
                j+=1
        line = f1.readline()
    f1.close()

    f2 = open(name_path+'first_name_utf8.txt', 'r', encoding='utf-8')
    fw = open(name_path + 'data/family_name_pro.txt', 'w', encoding='utf-8')
    line = f2.readline()
    while line:
        line = line.split(',')
        if line[0] in word_count:
            frq = float(line[1])*2.6/word_count[line[0]]
        else:
            frq = 0.95
        if frq > 0.95:
            frq = 0.95
        line = f2.readline()
        fw.write(line[0]+' '+str(frq)+'\n')
    f2.close()
    fw.close()

def cal_full_name(name_path):
    fr = open(name_path+'full_name_gbk.txt','r')
    fw = open(name_path+'data/33name_count_gbk.txt','w')
    line = fr.readline()
    count = dict()
    while line:
        if line.__len__() == 4:
            if line[2:3] in count:
                count[line[2:3]]+=1
            else:
                count[line[2:3]] =1

        line = fr.readline()

    for i in count.keys():
        fw.write(i+' '+str(count[i])+'\n')
    fw.close()
    fr.close()

def init_name(name_path):
    f1 = open(name_path+'family_name_pro.txt','r',encoding='utf-8')
    line = f1.readline()
    while line:
        line = line.split(' ')
        family_name_prob[line[0]]=float(line[1])
        line = f1.readline()
    f1.close()

    f1 = open(name_path+'22name_count_utf8.txt','r',encoding='utf-8')
    line = f1.readline()
    while line:
        line = line.split(' ')
        name22[line[0]]=int(line[1])
        line = f1.readline()
    f1.close()

    f1 = open(name_path+'32name_count_utf8.txt','r',encoding='utf-8')
    line = f1.readline()
    while line:
        line = line.split(' ')
        name32[line[0]]=int(line[1])
        line = f1.readline()
    f1.close()

    f1 = open(name_path+'33name_count_utf8.txt','r',encoding='utf-8')
    line = f1.readline()
    while line:
        line = line.split(' ')
        name33[line[0]]=int(line[1])
        line = f1.readline()
    f1.close()

def isname(str):
    try:
        str[2] == ' '
        if str[0] in family_name_prob and str[1] in name32 and str[2] in name33:
            prob = family_name_prob[str[:1]]*name32[str[1]]*name33[str[2]]
        else:
            prob =0.0
        if prob >6000:
            return True
        else:
            return False
    except IndexError:
        if str[0] in family_name_prob and str[1:] in name22:
            prob = family_name_prob[str[:1]]*name22[str[1:]]
        else:
            prob = 0.0
        if prob > 100:
            return True
        else:
            return False

path = 'D:/NLP/source.txt'
name_path = 'D:/NLP/data/'
family_name_prob = dict()
name22 = dict()
name32 = dict()
name33 = dict()
init_name(name_path)
f = open(name_path+'test.txt','r',encoding='utf-8')
line = f.readline()
line = f.readline()
while line:
    print(isname(line[:-1]))
    line = f.readline()
f.close()