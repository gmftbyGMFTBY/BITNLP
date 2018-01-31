#!/usr/bin/python3

import hashlib
import glob

# 结果输出
def print_split(text, point):
    for i, j in enumerate(text):
        if i in point:
            print(j + '/ ', end='')
        else:
            print(j, end='')
    print()

# 最大后项匹配
def BMM(text, book):
    points = []
    length = len(text)
    points.append(length - 1)
    index = len(text) - 1
    word_length = 5
    minus = index + 1
    while minus > 1:
        m = word_length
        if minus < m:
            m = minus
        while m != 0:
            word = text[(index - m + 1):(index + 1)]
            md5 = hashlib.md5()
            md5.update(word.encode('utf8'))
            s = md5.digest()
            if book.get(s, []) != [] and word in book[s]:
                points.append(index - m)
                index = index - m
                break
            elif m == 1:
                points.append(index - 1)
                index -= 1
            else:
                m -= 1
        minus = index + 1
        print(' ' * 50, end='\r')
        print('Processing ... ', "%.2f" % ((length - index) * 1.0 / length), end='\r')
    points.reverse()
    points[0:1] = []
    return points

# 最大正向匹配
def FMM(text, book):
    points = []    # the break point for the word
    index = 0
    word_length = 5    # the length of the word
    length = len(text)
    minus = length - index
    while minus > 1:
        m = word_length
        if minus < m :
            m = minus
        while m != 0:
            word = text[index:(index + m)]
            md5 = hashlib.md5()
            md5.update(word.encode('utf8'))
            s = md5.digest()
            if book.get(s, []) != [] and word in book[s]:
                points.append(index + m - 1)
                index += m
                break
            elif m == 1:
                points.append(index)
                index += 1
            else:
                m -= 1
        minus = length - index
        print(' ' * 50, end='\r')
        print('Processing ... ', '%.2f' % (index * 1.0 / length), end='\r')
    return points

# 条件概率计算
def calculate(list1, list2, ans, begin, end):
    # calculate for list1
    p = 1
    for i, j in list1[1:]:
        number1 = ans.count(list1[i - 1] + j)
        number2 = ans.count(list1[i - 1])
        p = p * number1 / number2
    q = 1
    for i, j in list2[1:]:
        number1 = ans.count(list2[i - 1] + j)
        number2 = ans.count(list2[i - 1])
        q = q * number1 / number2
    return p, q

# begin is the index of the begin of the sentence 
# end is the index of the ending of the sentence 
def n_gram(point1, point2, ans, begin, end):
    record = -1
    b1 = 0
    e1 = 0
    b2 = 0
    e2 = 0
    list1 = ['<BOS>']
    list2 = ['<BOS>']
    points = []
    for i, j in ans:    # scan the ans
        if i not in point1:
            if i not in point2:
                e1 += 1
                e2 += 1
            else:
                list2.append(ans[b2:(e2 + 1)])
                e2 += 1
                b2 = e2
                e1 += 1
        else:
            if i not in point2:
                list1.append(ans[b1:(e1 + 1)])
                e1 += 1
                b1 = e1
                e2 += 1
            else:
                list1.append(ans[b1:(e1 + 1)])
                e1 += 1
                b1 = e1
                list2.append(ans[b2:(e2 + 1)])
                e2 += 1
                b2 = e2
                count1, count2 = calculate(list1, list2, ans, begin, end)
                if count1 > count2 :
                    p1 = point1.index(record)
                    p2 = point1.index(i)
                    points.extend(point1[(p1 + 1):(p2 + 1)])
                else:
                    p1 = point2.index(record)
                    p2 = point2.index(i)
                    points.extend(point2[(p1 + 1):(p2 + 1)])
                record = i

if __name__ == '__main__':
    words = []
    linenumber = 0
    with open('/home/lantian/Downloads/BIT/NLP/Source/shanxi.txt', 'r', encoding='utf16') as f:
        string = f.read()
        words.extend(string.split())

    print('the len from the shanxi : ', len(words))

    book = {}
    for i in words:
        md5 = hashlib.md5()
        md5.update(i.encode('utf8'))
        ans = md5.digest()
        try:
            if i not in book[ans]:
                book[ans].append(i)
        except:
            book[ans] = [i]
 
    with open('/home/lantian/Downloads/BIT/NLP/Source/shanxi.txt', 'r', encoding='utf16') as f:
        string = f.read()
        linenumber = string.count('\n')
        # get the whole string from ans
        ans = ''.join(string.split())

    # ans = '我认为我是一个合格的党员，不管三七二十一，我认为我可以拯救世界，包括找到我爱的人，这就是我一生的梦想'
    # ans = '他是研究生物化学的'
    # ans = '我们的士兵同志想要下去吃饭'
    point1 = BMM(ans, book)
    print(point1[:10])
    point1 = set(point1)
    f = open('/home/lantian/Downloads/BIT/NLP/Source/answer.txt', 'r')
    w = f.read()
    ns = w.split()
    b = []
    for i in ns:
        b.append(int(i))
    b = set(b)
    a = point1 & b
    print(len(a) * 1.0 / len(point1))
    # 训练集下精确率95%
