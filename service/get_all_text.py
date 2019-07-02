#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/8 22:34
# @Author : ActStrady@tom.com
# @FileName : get_all_text.py
# @GitHub : https://github.com/ActStrady/wordcloud-steganography
import requests
from bs4 import BeautifulSoup


def get_text(url):
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text.strip(), 'html.parser')
    name = url[len('https://'):url.index('/', len('https://'), len(url))]
    path = '../html/{}.txt'.format(name)
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(soup.text.strip())
    return path
