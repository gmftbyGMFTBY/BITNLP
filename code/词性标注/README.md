﻿实现成员：郭佳楠（KanSunny）

##########################

BP_NN.py

	BP学习的三层感知机，实现词性标注功能
	
	具体实现算法，见上层algorithm文件夹

corpus.txt
	
	经过融合的北大2014语料库（含词性标注）

	实验中由于时间原因，仅训练了前300,000的数据	

lable_rule.txt

	北大2014语料库中使用的标注集共125个

word_pos.json

	北大2014语料库中词语及词语在标注集上的条件概率

ho_weight.txt

	隐含层-输出层之间的权重矩阵

ih_weight.txt

	输入层-隐含层之间的权重矩阵

using.txt

	测试集

correct.txt

	测试集结果

	以python list形式存储，便于后续操作
	
word_sign.json

	HMM词语输出概率
	
fore_arr.json

	词性转移概率

神经网络正确率.png

	仅进行1/7训练集，仅训练一遍后的正确率

	（可以增加训练、以及增加输入词语个数*进行提升）

规则修订的神经网络正确率.png

提示：运行时可能需修改本机路径

###########################

Created on 2018年1月16日

@author: KanSunny

###########################