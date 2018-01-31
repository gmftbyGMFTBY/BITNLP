#!/usr/bin/python3

# local file:train1

#************************************************
# n-gram与BMM，FMM结合的分词方式
# 与纯BMM相比，准确率提高了0.5%
# 可以增加语料库以提高准确率
# 接受UTF-8格式的语料库
# modification:    Dec,29 14:02
#************************************************

#************************************************
# function:    create the dict and the n-gram module
# parament:    the whole corpus
# influence:   change the variable prob1,prob2
#************************************************

#import isname
import re

prob_b = dict()
prob_n = dict()

def train(path):
    _index = dict()
    f1 = open(path,'r',encoding='utf-8')
    line = f1.readline()
    error_times =0
    
    line_counter = 0
    
    while line:
        prior = ''
        for word in line.split(' '):
            if word.__len__()> 20:
                continue
            if word in _index:
                _index[word]+=1
            else:
                _index[word]=1
            if prior != '':
                if prior not in times_n:
                    times_n[prior] = dict()
                if word in times_n[prior]:
                    times_n[prior][word]+=1
                else:
                    times_n[prior][word] = 1

                if word not in times_b:
                    times_b[word] = dict()
                if prior in times_b[word]:
                    times_b[word][prior]+=1
                else:
                    times_b[word][prior] = 1
            prior=word
        try:
            line = f1.readline()    # loop for lines
            line_counter += 1
        except UnicodeDecodeError:
            error_times+=1
            print(error_times)
        print("%d line has been processed !" % line_counter)
    f1.close()
    for i in _index.keys():
        if i in index:
            index[i]+=_index[i]
        else:
            index[i]=_index[i]

#************************************************
# function:    return the split result by FMM
# parament:    text:    a string need to be split
# influence:   nothing
#************************************************
def FMM(text):
    list = []
    i = 0        
    number = '２０７６１９５８４３1234567890'
    while text[i:].__len__()>=1:
        j = text[i:].__len__()

        # test for chinese number
        try:
            begin = i
            while text[i] in number:
                i += 1
                if i == text.__len__():
                    break
            if i != begin:
                list.append(text[begin:i])
                continue
        except:
            print('FMM Error !')
            exit(1)

        if j > Max_str:
            j = Max_str
        while j > 1:
            if text[i:i+j] in index:
                break
            '''
            if len(text[i:i+j]) == 2 or len(text[i:i+j]) == 3:
                res = isname.isname(text[i:i+j])
                if res == True:
                    break
            '''
            j -= 1
        list.append(text[i:i+j])
        i+=j
    return list

#************************************************
# function:    return the split result by BMM
# parament:    text:    a string need to be split
# influence:   nothing
#************************************************
def BMM(text):
    list = []
    i = text.__len__()
    number = '２０７６１９５８４３1234567890'
    while text[:i].__len__()>=1:
        j = text[:i].__len__()

        # test for chinese number
        begin = i
        while text[i-1] in number:
            i -= 1
            if i == 0 : 
                break
        if i != begin:
            list.append(text[i:begin])
            continue

        if j > Max_str:
            j = Max_str
        # the judge has aleardy changed
        while j > 1:
            if text[i-j:i] in index and text[i-j] not in number:
                break
            '''
            if len(text[i-j:i]) == 2 or len(text[i-j:i]) == 3:
                res = isname.isname(text[i-j:i]) 
                if res == True:
                    break
            '''
            j -=1
        list.append(text[i-j:i])
        i-=j
    return list[::-1]

#************************************************
# function:    use 2-gram to compare 2 kins of algorithms
# parament:    text:    a string need to be split
# influence:   nothing
#************************************************
def n_gram(text):
    # add two possibility
    
    global prob_b
    global prob_n
    global index
    
    ans1 = FMM(text)
    ans2 = BMM(text)
    i = 0
    j = 0
    while i<ans1.__len__() and j<ans2.__len__() and ans1[i]==ans2[j]:
        i+=1
        j+=1
    if i == ans1.__len__():
        return ans1
    start1 = i
    start2 = i
    i = 0
    j = 0
    while i<ans1.__len__() and j<ans2.__len__() and ans1[::-1][i] == ans2[::-1][j] :
        i+=1
        j+=1
    end1 = ans1.__len__() - i-1
    end2 = ans2.__len__() - i-1
    prob1 = 1.0
    prob2 = 1.0
    if start1 >= 1:
        for i in range(start1,end1+1):
            if ans1[i-1] not in prob_n:
                prob1 *= 0.000001
                continue
            if ans1[i] not in prob_n[ans1[i-1]]:
                # prob1 *= 0.000001/index[ans1[i-1]]
                prob1 *= 0.0000001 / index[ans1[i-1]]
                continue
            prob1 *= prob_n[ans1[i-1]][ans1[i]]
    else:
        for i in range(start1+1,end1+1):
            if ans1[i-1] not in prob_n:
                prob1 *= 0.000001
                continue
            if ans1[i] not in prob_n[ans1[i-1]]:
                prob1 *= 0.0000001/index[ans1[i-1]]
                continue
            prob1 *= prob_n[ans1[i-1]][ans1[i]]
    if end2 < ans2.__len__()-1:
        for i in range(start2,end2+1):
            if ans2[i+1] not in prob_b:
                prob2 *= 0.000001
                continue
            if ans2[i] not in prob_b[ans2[i+1]]:
                prob2*=0.0000001/index[ans2[i+1]]
                continue
            prob2*=prob_b[ans2[i+1]][ans2[i]]
    else:
        for i in range(start2,end2):
            if ans2[i+1] not in prob_b:
                prob2 *= 0.000001
                continue
            if ans2[i] not in prob_b[ans2[i+1]]:
                prob2*=0.0000001/index[ans2[i+1]]
                continue
            prob2*=prob_b[ans2[i+1]][ans2[i]]
    print(prob1,prob2)
    if prob1 > prob2:
        return ans1
    return ans2

#************************************************
# function:    get a .txt file and split
# parament:    path:    the path of text file
# return  :    以空格分隔好的字符串
# influence:   nothing
# edit time:   Dec,29, 13:59
#************************************************
def split(path):
    result = ''
    f = open(path, 'r',encoding='utf-8')
    text = f.readline()

    while text:
        try:
            # list = text.split('，')
            list = re.split('([，。！？“”《》{}【】()-=@#￥%……&×～`])', text)
            temp = list.__len__()
            for sentence in list:
                if BMM(sentence) == FMM(sentence):
                    ans = BMM(sentence)
                else:
                    ans = n_gram(sentence)
                for i in ans:
                    result += i
                    result += ' '
            text = f.readline().replace(' ', '')
        except UnicodeDecodeError:
            temp = 0
    return result

# just for debuging ... 
def test_split(path):
    result = ''
    f = open(path, 'r', encoding='utf-8')
    text = f.readline()

    while text:
        try:
            # list = text.split('，')
            list = re.split('([，。！？“”《》{}【】()-=@#￥%……&×～`])', text)
            temp = list.__len__()
            for sentence in list:
                if BMM(sentence) == FMM(sentence):
                    ans = BMM(sentence)
                else:
                    ans = FMM(sentence)
                for i in ans:
                    result += i
                    result += ' '
            text = f.readline().replace(' ', '')
        except UnicodeDecodeError:
            temp = 0
    return result
    
# 将训练的模型写入文件中，加快速度
def save_module():
    import pickle
    # save the prob_b / prob_n
    with open('pron_b.pkl', 'wb') as f:
        pickle.dump(prob_b, f)
    
    print("Have been writed to the file pron_b.pkl")
    
    with open('pron_n.pkl', 'wb') as f:
        pickle.dump(prob_n, f)
    print("Have been writed to the file pron_n.pkl")
    
    # we can switch the dict
    with open('index_new.pkl', 'wb') as f:
        pickle.dump(index, f)
    print("Have been writed to the file index.pkl")
    
    return True

def read_module():
    # read the module from the file
    import pickle
    with open('pron_b.pkl', 'rb') as f:
        prob_b = pickle.load(f)
    
    with open('pron_n.pkl', 'rb') as f:
        pron_n = pickle.load(f)
    
    with open('index.pkl', 'rb') as f:
        index = pickle.load(f)
        
    print('read the file successfully !')
    return prob_b, prob_n, index

def get_index(target):
    # get the target & calculate the result
    index = []
    s     = 0
    for i in target:
        s += len(i)
        index.append(s)
    return index

def calculate(mine_str):
    # calculate the result
    print("begin to caluculating ... ") 
    with open('./3.txt',encoding='utf-8') as f:
        #try:
        content = f.read()
        res = content.split()
        #except UnicodeDecodeError:
            #pass

    # res is the split result
    
    # mine split result
    mine_res = mine_str.split()
    
    res1 = set(get_index(res))
    res2 = set(get_index(mine_res))
    
    res = res1 & res2
    P = round(len(res) / len(res2), 4)
    R = round(len(res) / len(res1), 4)
    return P, R

#************************************************
# 使用方法   : 将测试文本的文件路径提供给split函数
# 注意       : 全程UTF-8编码
#************************************************
if __name__ == "__main__":
    # train the module and save the module into two file prob_b.pkl, prob_n.pkl
    Max_str = 15                    # the max length of one word


    # 加入数字识别之后，正确率上升 0.5 % 

    path = './source.txt'           # training    ???
    index = dict()                  # all word 
    times_b = dict()
    times_n = dict()
    # training the module
    print("Begin to train ... ")
    train(path)    
    # forward
    for i in times_n.keys():
        if i not in prob_n:
            prob_n[i] = dict()
        for j in times_n[i].keys():
            prob_n[i][j] = times_n[i][j] * 1.0 / index[i]
            
    # back
    del times_n
    for i in times_b.keys():
        if i not in prob_b:
            prob_b[i] = dict()
        for j in times_b[i].keys():
            prob_b[i][j] = times_b[i][j] * 1.0 / index[i]
    del times_b
    
    # save the moduel into the binary file
    # save_module()
    # read the module
    # global prob_b
    # global prob_n
    # global index

    # isname.init_name('./name_data/')
    # prob_b, prob_n, index = read_module()
    # test 
    
    test_path = './4.txt'
    string = split(test_path)
    with open('result.txt', 'w') as f:
        f.write(string)
    P, R = calculate(string)
    print(P, R)
