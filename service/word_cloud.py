#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/8 16:11
# @Author : ActStrady@tom.com
# @FileName : word_cloud.py
# @GitHub : https://github.com/ActStrady/wordcloud-steganography
import os
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import jieba


def wl(in_path, in_image):
    d = path.dirname(__file__)
    # 读取文件文字
    text = open(path.join(d, in_path), encoding='utf-8').read()

    # 打开一张现有图片
    alice_mask = np.array(Image.open(path.join(d, in_image)))

    # 词云生成
    stopwords = set(STOPWORDS)
    stopwords.add("said")
    wc = WordCloud(font_path='simhei.ttf', background_color="white", max_words=2000, mask=alice_mask,
                   stopwords=stopwords)
    # 使用jieba来中文分词
    word_list = jieba.cut(text, cut_all=True)
    wl_space_split = " ".join(word_list)

    # 输出图片
    wc.generate(wl_space_split)
    # 图片名处理
    long_name = os.path.split(in_path)[1]
    name = os.path.splitext(long_name)[0]
    # 图片存为本地
    path_ = path.join(d, '../image/word_cloud/{}.png'.format(name))
    wc.to_file(path_)
    return path_
