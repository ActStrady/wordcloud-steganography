#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/9 0:06
# @Author : ActStrady@tom.com
# @FileName : steganography.py
# @GitHub : https://github.com/ActStrady/wordcloud-steganography
from PIL import Image


def makeImageEven(image):
    """
    取得一个 PIL 图像并且更改所有值为偶数（使最低有效位为0）
    """
    # 得到一个这样的列表：[(r,g,b,t),(r,g,b,t)...]
    pixels = list(image.getdata())
    print(pixels)
    # 更改所有值为偶数（魔法般的移位）
    evenPixels = [(r >> 1 << 1, g >> 1 << 1, b >> 1 << 1) for [r, g, b] in pixels]
    # 创建一个相同大小的图片副本
    evenImage = Image.new(image.mode, image.size)
    # 把上面的像素放入到图片副本
    evenImage.putdata(evenPixels)
    return evenImage


def constLenBin(int):
    """
    内置函数bin()的替代，返回固定长度的二进制字符串
    """
    # 去掉bin()返回的二进制字符串中的'0b'，并在左边补足'0'直到字符串长度为8
    binary = "0" * (8 - (len(bin(int)) - 2)) + bin(int).replace('0b', '')
    return binary


def encodeDataInImage(image, data):
    """
    将字符串编码到图片中
    """
    # 获得最低有效位为 0 的图片副本
    evenImage = makeImageEven(image)
    # 将需要被隐藏的字符串转换成二进制字符串
    binary = ''.join(map(constLenBin, bytearray(data, 'utf-8')))
    if len(binary) > len(image.getdata()) * 4:
        # 如果不可能编码全部数据，跑出异常
        raise Exception("Error: Can't encode more than" + str(len(evenImage.getdata()) * 4) + " bits in this image. ")
    # 将binary中的二进制字符串信息编码进像素里
    encodedPixels = [(r + int(binary[index * 4 + 0]), g + int(binary[index * 4 + 1]), b + int(binary[index * 4 + 2])) if index * 4 < len(binary) else (r, g, b) for
                     index, (r, g, b) in enumerate(list(evenImage.getdata()))]
    # 创建新图片以存放编码后的像素
    encodedImage = Image.new(evenImage.mode, evenImage.size)
    # 添加编码后的数据
    encodedImage.putdata(encodedPixels)
    return encodedImage


def binaryToString(binary):
    """
    从二进制字符串转为 UTF-8 字符串
    """
    index = 0
    string = []
    rec = lambda x, i: x[2:8] + (rec(x[8:], i - 1) if i > 1 else '') if x else ''
    fun = lambda x, i: x[i + 1:8] + rec(x[8:], i - 1)
    while index + 1 < len(binary):
        chartype = binary[index:].index('0')  # 存放字符所占字节数，一个字节的字符会存为0
        length = chartype * 8 if chartype else 8
        string.append(chr(int(fun(binary[index:index + length], chartype), 2)))
        index += length
    return ''.join(string)


def decodeImage(image):
    """
    解码隐藏数据
    """
    pixels = list(image.getdata())  # 获得像素列表
    # 提取图片中所有最低有效位中的数据
    binary = ''.join([str(int(r >> 1 << 1 != r)) + str(int(g >> 1 << 1 != g)) + str(int(b >> 1 << 1 != b)) for (r, g,
                                                                                                                b) in pixels])
    # 找到数据截止处的索引
    locationDoubleNull = binary.find('0000000000000000')
    endIndex = locationDoubleNull + (
                8 - (locationDoubleNull % 8)) if locationDoubleNull % 8 != 0 else locationDoubleNull
    data = binaryToString(binary[0:endIndex])
    return data


# encodeDataInImage(Image.open("coffee.png"), '哆啦A梦的世界，Doraemon World!').save('encodeImage.png')
#
# print(decodeImage(Image.open("encodeImage.png")))
