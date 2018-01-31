## 文本摘要

---

1. 项目基本信息

   >1. Python 3.6
   >
   >2. 依赖库
   >
   >   * bs4
   >
   >   * numpy
   >
   >   * jieba : 
   >
   >     分词方面为了保证程序的速度，我们测试使用jieba库，在实际使用中可以更换成大作业一中的小组设计的分词程序
   >
   >3. 使用平台 : 
   >
   >   如果不运行GUI界面，可以考虑任何平台运行
   >
   >   GUI程序中调用了Linux系统可执行程序，使用GUI请在Linux系统下运行

2. 组员信息和分工

   1. 兰天

      >1. ID : 1120151828
      >2. Nickname : GMFTBY
      >3. Task
      >   1. TextRank算法实现
      >   2. 作业GUI界面
      >   3. 数据集的获取和处理分析

   2. 肖子原

      >1. ID : 1120151861
      >2. Nickname : Shaw
      >3. Task
      >   1. MMR算法实现
      >   2. 分析测试摘要结果

   3. 郭佳楠

      >1. ID : 1120151825
      >2. Nickname : KanSunny
      >3. Task
      >   1. TF-IDF算法实现
      >   2. 余弦相似度和TextRank相似度

3. 代码文件结构

   1. 数据集

      1. `news_result.txt` 搜狗新闻数据集

         使用搜狗实验室(Sogou Labs)提供的文本数据集(新闻数据)，对其实现摘要，参考摘要实验数据使用因为网上找不到合适的数据集，采用我们三个人的参考摘要的均值实现

      2. `stopwords` : 中文停用词文件

      3. `result` : 摘要结果存放目录

   2. 代码结构

      1. `MMR.py` : MMR算法模块
      2. `TFIDF.py` : TF-IDF算法模块
      3. `analyser.py` : 内部测试模块，使用Edmundson评测方法
      4. `visual.py` : GUI界面程序(因为tkinter对中文支持的不友好，请尽量不要使用，或者使用其中的edit功能实现预览,请一定在`Linux`系统下运行该程序)
      5. `dataset.py` : 数据集获取脚本
      6. `TextRank.py` : **项目主入口，可以直接运行，GUI程序只是实现了对其的封装**