#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/8 10:27
# @Author : ActStrady@tom.com
# @FileName : main_view.py
# @GitHub : https://github.com/ActStrady/wordcloud-steganography
import os
from tkinter import *
from tkinter.filedialog import askopenfilename

from PIL import ImageTk
from PIL import Image

from service import word_cloud
from service import get_all_text
from service import steganography

path = ''


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


def wl():
    path_ = word_cloud.wl(path, '../resources/images.jpeg')
    show_image(path_)


def open_file():
    global path
    path = askopenfilename()
    file_name = os.path.split(path)[1]
    file_type = os.path.splitext(file_name)[1]
    text_list = ('.txt', '.md', '.sql')
    image_list = ('.jpeg', '.jpg', '.png', '.gif')
    if file_type in text_list:
        show_text(path)
    elif file_type in image_list:
        show_image(path)
    else:
        content.delete('1.0', 'end')
        content.insert(INSERT, '文件类型暂不支持')


def show_text(path_):
    text = open(path_, encoding='utf-8').read()
    content.delete('1.0', 'end')
    content.insert(INSERT, text)


def show_image(path_):
    image = Image.open(path_)
    photo = ImageTk.PhotoImage(image)
    content.delete('1.0', 'end')
    content.image_create(INSERT, image=photo)
    content.image = photo


def url_text():
    url = entry.get()
    if url is not '':
        global path
        path = get_all_text.get_text(url)
        show_text(path)


def steg():
    long_name = os.path.split(path)[1]
    name = os.path.splitext(long_name)[0]
    steganography.encodeDataInImage(Image.open(path), path).save('../image/steganography/{}.png'.format(name))
    show_image('../image/steganography/{}.png'.format(name))
    global st_path
    st_path = '../image/steganography/{}.png'.format(name)


def steg_reduction():
    text = steganography.decodeImage(Image.open(st_path))
    content.delete('1.0', 'end')
    content.insert(INSERT, text)


# 主窗口
root = Tk()
root.title('词云与隐写术')
center_window(root, 450, 450)
root.resizable(False, False)

# pack布局
top = Frame(root)
entry = Entry(top, width=30)
entry.pack(side=LEFT)
Button(top, text='解析', command=url_text).pack(side=LEFT)
Button(top, width=20, text='打开文件', command=open_file).pack(side=RIGHT)
top.pack(fill=X, anchor=N, padx=5, pady=10)

content = Text(root)
content.pack(expand=YES, fill=BOTH, padx=40, pady=10)

bottom = Frame(root)
Button(bottom, width=20, text='生成词云', command=wl).pack(side=LEFT)
Button(bottom, text='生成隐写', command=steg).pack(side=RIGHT)
Button(bottom, text='还原隐写', command=steg_reduction).pack(side=RIGHT)
bottom.pack(side=BOTTOM, fill=X, anchor=N, padx=50, pady=10)

root.mainloop()
