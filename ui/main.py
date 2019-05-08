#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/8 10:27
# @Author : ActStrady@tom.com
# @FileName : main.py
# @GitHub : https://github.com/ActStrady/wordcloud-steganography
from tkinter import *


def center_window(window, width, height):
    """
    居中窗口
    :param window:
    :param width:
    :param height:
    :return:
    """
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)


# 主窗口
root = Tk()
root.title('词云与隐写术')
center_window(root, 450, 400)
root.resizable(False, False)

# pack布局
top = Frame(root)
Entry(top, width=40).pack(side=LEFT)
Button(top, width=20, text='打开文件').pack(side=RIGHT)
top.pack(fill=X, anchor=N, padx=5, pady=20)

Label(root, bg='red').pack(expand=YES, fill=BOTH, padx=60, pady=20)

bottom = Frame(root)
Button(bottom, width=20, text='生成词云').pack(side=LEFT)
Button(bottom, width=20, text='还原隐写').pack(side=RIGHT)
bottom.pack(side=BOTTOM, fill=X, anchor=N, padx=50, pady=20)

mainloop()
