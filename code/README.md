# 使用方式
### 分词

1. `source.txt` : 训练集

2. `GMFTBY.py` : 训练脚本

3. `code.py` : 

   * **实际运行脚本**，其中使用`BMM`, `FMM`, `N-gram`三种算法
   * 运行`code.py`生成文件`result.txt`
   * **请将测试集文件名称命名为4.txt**

4. `result.txt`

   是一个使用空格分开的对测试集的分词结果

### 词性标注

`BP_NN.py` : 实际的运行脚本

* 输入文件是分词后的文件(见`分词`)，并命名为`using.txt`
* 输出文件是`correct.txt`，文件内是词性标注的结果


### 命名实体识别

1. `source.txt` : 内部使用了针对`数字`的命名实体识别
2. 分词文件夹下`isname.py`使用了针对`中文人名`的命名实体识别
3. 效果
   * 数字的命名实体识别，使得精确率提高了 `0.5%`
   * 中文任命的命名实体识别的效果不是很好，结果是对人名做了很好的识别，但是对与原来正确的语句产生了误切的影响