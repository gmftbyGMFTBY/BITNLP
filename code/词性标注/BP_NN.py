'''
Created on 2017年12月23日

@author: KanSunny
'''

import math
import random
import json

random.seed(0)

#################################
# 工具函数
# 生成（a，b）随机数
def rand(a, b):
    return (b - a) * random.random() + a

# 创建m*n的填充为fill的指定矩阵
def make_matrix(m, n, fill=0.0):    
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat

# 定义激活函数
def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

# 计算激活函数的导数
def sigmoid_derivative(x):
    return x * (1 - x)
###################################

##################################
# 使用三个列表维护输入层、隐含层、输出层神经元
# 列表中元素代表神经元当前的输出值
# 使用两个二维矩阵维护输入层与隐含层，隐含层与输出层之间的权值
class BPNeuralNetwork:
    def __init__(self):
        self.input_n = 0#输入层、隐含层、输出层神经元个数
        self.hidden_n = 0
        self.output_n = 0
        self.input_cells = []#各类神经元输出
        self.hidden_cells = []
        self.output_cells = []
        self.input_weights = []#权重矩阵
        self.output_weights = []
        self.input_correction = []#上一次纠错矩阵
        self.output_correction = []
        # 词被标注为相应词性的次数
        word_sign = {}
        # fi前面被标注为fi-1的次数
        fore_arr = {}
        # 词性出现的次数
        appear_times = []
    
    # 初始化神经网络
    def setup(self, ni, nh, no):
        self.input_n = ni + 1#增加一个偏置神经元
        self.hidden_n = nh
        self.output_n = no
        # 初始化神经元输出全为1.0
        self.input_cells = [1.0] * self.input_n
        self.hidden_cells = [1.0] * self.hidden_n
        self.output_cells = [1.0] * self.output_n
        # 创建权重矩阵
        self.input_weights = make_matrix(self.input_n, self.hidden_n)
        self.output_weights = make_matrix(self.hidden_n, self.output_n)
        # 随机初始化权重矩阵
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weights[i][h] = rand(-0.2, 0.2)
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                self.output_weights[h][o] = rand(-2.0, 2.0)
        # 创建上一次纠错矩阵
        self.input_correction = make_matrix(self.input_n, self.hidden_n)
        self.output_correction = make_matrix(self.hidden_n, self.output_n)
    
    # 进行一次前馈并返回输出
    def predict(self, inputs):
        # 输入层神经元输入值，也是输出值
        for i in range(self.input_n - 1):
            self.input_cells[i] = inputs[i]
        # 计算隐含层神经元输出值
        for j in range(self.hidden_n):
            total = 0.0
            for i in range(self.input_n):#计算隐含层神经元输入值
                total += self.input_cells[i] * self.input_weights[i][j]
            self.hidden_cells[j] = sigmoid(total)#计算隐含层神经元输出值
        # 计算输出层神经元的输出值
        for k in range(self.output_n):
            total = 0.0
            for j in range(self.hidden_n):
                total += self.hidden_cells[j] * self.output_weights[j][k]
            self.output_cells[k] = sigmoid(total)
        return self.output_cells[:]

    # 进行一次反向传播
    def back_propagate(self, case, label, learn, correct):
        # 前馈得到隐含层与输出层输出
        self.predict(case)
        # 获取输出层误差
        output_deltas = [0.0] * self.output_n
        for o in range(self.output_n):
            error = label[o] - self.output_cells[o]
            output_deltas[o] = sigmoid_derivative(self.output_cells[o]) * error
        # 获取隐含层误差
        hidden_deltas = [0.0] * self.hidden_n
        for h in range(self.hidden_n):
            error = 0.0
            for o in range(self.output_n):
                error += output_deltas[o] * self.output_weights[h][o]
            hidden_deltas[h] = sigmoid_derivative(self.hidden_cells[h]) * error
        # 更新隐含层与输出层之间的权重
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                change = output_deltas[o] * self.hidden_cells[h]
                self.output_weights[h][o] += learn * change + correct * self.output_correction[h][o]#更新权重
                self.output_correction[h][o] = change#更新纠错矩阵
        # 更新输入层与隐含层之间的权重
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                change = hidden_deltas[h] * self.input_cells[i]
                self.input_weights[i][h] += learn * change + correct * self.input_correction[i][h]
                self.input_correction[i][h] = change

    # 训练
    def train(self, limit, learn=0.05, correct=0.1):
        self.setup(375, 100, 125)
        words = []
        labels = []
        word_pos = {}
        # 训练集
        with open('./corpus.txt', 'r', encoding = 'utf8') as fp:
            string = []
            string = fp.read()
            words = string.split()
        length = len(words)
        # 词的概率表
        with open('./word_pos.json', 'r', encoding = 'utf8') as fp:
            word_pos = json.load(fp)    
        # 标注集
        with open('./lable_rule.txt', 'r', encoding = 'utf8') as fp:
            string = []
            string = fp.read()
            labels = string.split()
        
        for j in range(limit):
            word_num = 0
            num = 0
            case = []
            label = [0.0 for n in range(125)]
            zero = [0.0 for n in range(125)]
            while word_num < 300000:
                word = words[word_num]
                word_num += 1
                temp = []
                temp = word.split('/')
                num += 1
                print(word_num)
                if temp[0] in word_pos:
                    case.extend(word_pos[temp[0]])
                else:
                    case.extend(zero)
                if num == 2:
                    for i in range(len(labels)):
                        if labels[i] == temp[1]:
                            label[i] += 1.0
                            break
                if num%3 == 0:
                    self.back_propagate(case, label, learn, correct)
                    case[:] = []
                    label = [0.0 for n in range(125)]
                    num = 0
                    word_num = word_num-2
            print(j) 
        with open('./ho_weight.txt', 'a', encoding = 'utf8') as fp:
            for h in range(self.hidden_n):
                for o in range(self.output_n):
                    fp.write(str(self.output_weights[h][o])+' ')
                    
        with open('./ih_weight.txt', 'a', encoding = 'utf8') as fp:
            for i in range(self.input_n):
                for h in range(self.hidden_n):
                    fp.write(str(self.input_weights[i][h])+' ')

# 基于规则的HMM算法
    def hmm(self,test_str):
        # 标注的最大概率
        Tmax = 0
        # 最大概率对应的标注序号
        Tnum = 126
        zero = [0.0 for n in range(125)]
    
        for i in range(125):
            a = (self.word_sign[test_str[0]][i])/((self.appear_times[i]+1)*1.0)
            if a == 0:
                continue
            for j in range(125):
                b = (self.fore_arr[str(j)][i] /((self.appear_times[i]+1)*1.0))*(self.word_sign[test_str[1]][j]/((self.appear_times[j]+1)*1.0))
                if b == 0:
                    continue
                for k in range(125):
                    c = (self.fore_arr[str(k)][j]/((self.appear_times[j]+1)*1.0))*(self.word_sign[test_str[2]][k]/((self.appear_times[k]+1)*1.0))
                    if c == 0:
                        continue
                    T = a*b*c*1.0
                    if(T > Tmax):
                        Tmax = T
                        Tnum = j
        #print('+++++')
        #print(Tnum)
        return Tnum

    # 测试训练集数据正确率（仅前馈）
    def test(self):
        self.setup(375, 100, 125)
        words = []
        labels = []
        word_pos = {}
        correct = 2
        # 训练集
        with open('./ho_weight.txt', 'r', encoding = 'utf8') as fp:
            string = []
            string = fp.read()
            string = string.split()
            for h in range(self.hidden_n):
                for o in range(self.output_n):
                    #print(h*self.output_n+o)
                    self.output_weights[h][o] = float(string[h*self.output_n+o])
                    
        with open('./ih_weight.txt', 'r', encoding = 'utf8') as fp:
            string = []
            string = fp.read()
            string = string.split()
            for i in range(self.input_n):
                for h in range(self.hidden_n):
                    #print(i*self.hidden_n+h)
                    self.input_weights[i][h] = float(string[i*self.hidden_n+h])
                
        with open('./corpus.txt', 'r', encoding = 'utf8') as fp:
            string = []
            string = fp.read()
            words = string.split()
        length = len(words)
        # 词的概率表
        with open('./word_pos.json', 'r', encoding = 'utf8') as fp:
            word_pos = json.load(fp)    
        # 标注集
        with open('./lable_rule.txt', 'r', encoding = 'utf8') as fp:
            string = []
            string = fp.read()
            labels = string.split()
        with open('./word_sign.json', 'r', encoding = 'utf8') as fp:
            self.word_sign = json.load(fp)
        with open('./fore_arr.json', 'r', encoding = 'utf8') as fp:
            self.fore_arr = json.load(fp)
        with open('./appear_times.json', 'r', encoding = 'utf8') as fp:
            self.appear_times = json.load(fp)
        #print('finish read')

        word_num = 0
        num = 0
        case = []
        label = [0.0 for n in range(125)]
        zero = [0.0 for n in range(125)]
        test_str = []
        hmm_num = 0
        flag = 0 # 是否出现未标注词
        #words = ['11@','22@','3@']
        while word_num < 3000:
            word = words[word_num]
            word_num += 1
            temp = []
            temp = word.split('/')
            num += 1
            print(word_num)
            if temp[0] in word_pos:
                case.extend(word_pos[temp[0]])
                test_str.append(temp[0])
            else:
                case.extend(zero)
                test_str.append('$')
                flag = 1 
            if num == 2:
                for i in range(len(labels)):
                    if labels[i] == temp[1]:
                        label[i] += 1.0
                        break
            if num%3 == 0:
                self.predict(case)
                a = max(self.output_cells)
                result = self.output_cells.index(a)
                self.output_cells[result] = 0
                b = max(self.output_cells)
                
                if a-b<0.085 and flag == 0:
                    #print(test_str)
                    result = self.hmm(test_str)
                    hmm_num += 1
                test_str.clear()
                flag = 0
                # 寻找规则和NN中处理最好的，作为标注
                #c = get_best(a,b)????
                if label.index(max(label)) == result:
                    correct += 1
                case[:] = []
                label = [0.0 for n in range(125)]
                num = 0
                word_num = word_num-2
        print(hmm_num)
        print(correct)
        print(correct/3000)


    def using(self, words):# 使用（仅前馈）
        self.setup(375, 100, 125)
        labels = []
        corrects = []
        length = len(words)
        corrects.extend(words) 
        
        # 输出级权重
        with open('./ho_weight.txt', 'r', encoding = 'utf8') as fp:
            string = []
            string = fp.read()
            string = string.split()
            for h in range(self.hidden_n):
                for o in range(self.output_n):
                    self.output_weights[h][o] = float(string[h*self.output_n+o])
        # 输入级权重            
        with open('./ih_weight.txt', 'r', encoding = 'utf8') as fp:
            string = []
            string = fp.read()
            string = string.split()
            for i in range(self.input_n):
                for h in range(self.hidden_n):
                    self.input_weights[i][h] = float(string[i*self.hidden_n+h])
        # 标注集
        with open('./lable_rule.txt', 'r', encoding = 'utf8') as fp:
            string = []
            string = fp.read()
            labels = string.split()
        # 可识别词    
        with open('./word_pos.json', 'r', encoding = 'utf8') as fp:
            word_pos = json.load(fp)    
        # 词的概率表
        with open('./word_pos.json', 'r', encoding = 'utf8') as fp:
            word_pos = json.load(fp)    
        # 标注集
        with open('./lable_rule.txt', 'r', encoding = 'utf8') as fp:
            string = []
            string = fp.read()
            labels = string.split()
        with open('./word_sign.json', 'r', encoding = 'utf8') as fp:
            self.word_sign = json.load(fp)
        with open('./fore_arr.json', 'r', encoding = 'utf8') as fp:
            self.fore_arr = json.load(fp)
        with open('./appear_times.json', 'r', encoding = 'utf8') as fp:
            self.appear_times = json.load(fp)
        #print('finish read')
        word_num = 0
        num = 0
        case = []
        zero = [0.0 for n in range(125)]
        test_str = []
        hmm_num = 0
        flag = 0 # 是否出现未标注词
        while word_num < length:
            word = words[word_num]
            word_num += 1
            num += 1
            if word in word_pos:
                case.extend(word_pos[word])
                test_str.append(word)
            else:
                case.extend(zero)
                test_str.append('$')
                flag = 1 
            print(word_num)
            if num%3 == 0:
                self.predict(case)
                a = max(self.output_cells)
                result = self.output_cells.index(a)
                self.output_cells[result] = 0
                b = max(self.output_cells)
                
                if a-b<0.085 and flag == 0: # 判断是否需要用HMM进行重标记
                    #print(test_str)
                    t1 = self.hmm(test_str)
                    if t1 != 126:
                        result = t1
                    hmm_num += 1
                test_str.clear()
                flag = 0
                
                temp = result
                temp = labels[temp]
                tw = corrects[word_num-2]
                tw += '/' + temp
                corrects[word_num-2] = tw
                case[:] = []
                label = [0.0 for n in range(125)]
                num = 0
                word_num = word_num-2
        with open('./correct.txt', 'a', encoding = 'utf8') as fp:
            fp.write(str(corrects))
        

if __name__ == '__main__':
    # 训练
    #nn_train = BPNeuralNetwork()
    #nn_train.train(1, 0.05, 0.1)
    
    # 测试
    #nn_test = BPNeuralNetwork()
    #nn_test.test()

    # 使用 请把已分词，但未进行词性标注的文本命名为using.txt，输出结果为correct.txt
    with open('./using.txt', 'r', encoding = 'utf8') as fp:    
        string = []
        string = fp.read()
        string = string.split()
        print('len of using txt:',len(string))
        nn_using = BPNeuralNetwork()
        nn_using.using(string)