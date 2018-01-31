#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.1.23

'''
请一定要在Linux下运行该脚本,调用了shell的命令，windows下会报错
可视化模块，使用tkinter包装实现的代码
* 因为Python的tkinter对中文的支持不是很友好，所以界面的表现比较简陋，所有我们添加了几个功能使得在Linux下的运行比较的舒服
    1. 对结果保存到文件
    2. 对结果的保存文件可以编辑
    3. 对之前的保存文件进行读取
    4. 利用Edmundson内部评估方法对编辑之后的参考的文本摘要做评分(功能仅供参考，因为在望山的搜索中没有找到合适的中文文本摘要的语料库的参考摘要，只能手动编辑)
'''

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext

# 导入编辑的计算模块
import TextRank as tr
import dataset
import TFIDF
import analyser

import os

class summary:
    def __init__(self):
        # 初始化框架
        self.window = tk.Tk()
        self.window.title("The summary")
        self.window.geometry('741x520')
        self.window.resizable(False, False)

        # 初始化菜单
        self.menubar = tk.Menu(self.window)
        self.window.config(menu = self.menubar)
        self.function_menubar = tk.Menu(self.menubar)
        self.menubar.add_cascade(label = 'Function', menu = self.function_menubar)

        self.function_menubar.add_command(label = 'Save', command = self.save)
        self.function_menubar.add_command(label = 'Edit', command = self.edit_with_vim)
        self.function_menubar.add_command(label = 'Calculate', command = self.calculate)
        
        self.function_menubar.add_command(label = 'Read', command = self.readfile)
        self.function_menubar.add_separator()
        self.function_menubar.add_command(label = 'Exit', command = self.window.destroy)
        
        # 初始化左右框架
        self.frm_r = tk.Frame(self.window)
        self.frm_r.place(x = 400, y = 0)
        self.frm_l = tk.Frame(self.window)
        self.frm_l.place(x = 0, y = 0)
        
        # 初始化右框架
        self.label = tk.Label(self.frm_r, text = 'Summary', bg = 'yellow',\
                              font = ('Arial', 12), width = 42, height = 2)
        self.label.grid(row = 0, column = 0)
        self.text_summary = scrolledtext.ScrolledText(self.frm_r, height = 35, width = 45)
        self.text_summary.grid(row = 1, column = 0)
        self.label = tk.Label(self.frm_r, text = 'Run', bg = 'yellow',\
                              font = ('Arial', 12), width = 42, height = 2)
        self.label.grid(row = 2, column = 0)
        self.button = tk.Button(self.frm_r, text = 'Run', width = 10, height = 2, \
                command = self.run)
        self.button.grid(row = 3, column = 0)
        
        # 初始化左框架
        self.label = tk.Label(self.frm_l, text = 'Answer', bg = 'yellow',\
                              font = ('Arial', 12), width = 42, height = 2)
        self.label.grid(row = 0, column = 0)
        self.text_answer = scrolledtext.ScrolledText(self.frm_l, height = 35, width = 45)
        self.text_answer.grid(row = 1, column = 0)
        self.label = tk.Label(self.frm_l, text = 'Result', bg = 'yellow',\
                              font = ('Arial', 12), width = 42, height = 2)
        self.label.grid(row = 2, column = 0)
        self.result_text = tk.Text(self.frm_l, height = 2, width = 20)
        self.result_text.grid(row = 3, column = 0)
        
        # 读写控制标志
        self.write_flag = False
        self.write_file_name = None
    
    def readfile(self):
        # 从文件中读取文本
        self.text_answer.delete(1.0, tk.END)
        self.text_summary.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
        
        fpath = filedialog.askopenfilename()
        sflag = False
        dflag = False
        with open(fpath) as f:
            sents = f.readlines()
            summary = []
            result  = []
            for sent in sents:
                if 'Summary' in sent:
                    sflag = True
                    continue
                elif 'Doc' in sent:
                    dflag = True
                    sflag = False
                    continue
                elif sflag :
                    summary.append(sent)
                elif dflag:
                    result.append(sent)
        self.fill_doc('。\n'.join(result))
        self.fill_summary('。\n'.join(summary))
        self.write_flag = True     # can edit now
        return True
        
    def fill_doc(self, doc):
        # 填充文本
        self.text_answer.insert('end', doc + '\n')
    
    def fill_summary(self, summary):
        # 填充摘要
        self.text_summary.insert('end', summary + '\n')        
    
    def run(self):
        # 读取语料库,运行摘要程序
        doc, index = dataset.read_sogou(1)
        
        # debug module
        # doc, index = dataset.read_test()
        summary = tr.summary(doc, index)
        
        # delete the text
        self.text_answer.delete(1.0, tk.END)
        self.text_summary.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
        
        # fill the text with the doc, summary
        self.fill_doc(doc)
        self.fill_summary(summary)
        
        self.window.update()    # show the result
        self.write_file_name = None
        self.write_flag      = False
        return 

    def start(self):
        # 开启主循环
        self.window.mainloop()

    def edit_with_vim(self):
        # 使用gedit在linux下对结果做编辑和预览，tkinter的界面对中文支持的太渣
        if not self.write_flag:
            messagebox.showerror(title = 'Fatal Error', message = 'You have not write the file, please write the file !')
            return False
        fpath = self.write_file_name
        ans = os.system('gedit %s' % fpath)
        if ans == 0 :
            print("Edit successfully !")
            return True
        else:
            print("Edit Unsuccessfully !")
            return False

    def save(self):
        # 保存文本
        self.write_file_name = filedialog.asksaveasfilename()
        with open(self.write_file_name, 'w') as f:
            # write the summary
            f.write("Summary : " + '-' * 20 + '\n')
            summary = self.text_summary.get(0.0, 'end')
            f.write(summary)
            f.write('Doc     : ' + '-' * 20 + '\n')
            doc = self.text_answer.get(0.0, 'end')
            f.write(doc)
        self.write_flag = True
        return True

    def calculate(self):
        # 计算评分
        summary = self.text_summary.get(0.0, 'end')
        doc = self.text_answer.get(0.0, 'end')
        result = round(analyser.Edmundson(summary, doc), 2)
        self.result_text.insert('insert', str(result))

if __name__ == "__main__":
    app = summary()
    app.start()
