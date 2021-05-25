# coding:utf-8

from collections import Counter
from os import path
import jieba
# 写入excel
import xlwt
# 引入正则表达式提取中文
import re

book = xlwt.Workbook()
sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

def remove(text):
    pattern = re.compile("[^\u4e00-\u9fa5]")  # 模式匹配所有中文字符

    return re.sub(pattern, '', text)

def word_segment(text):
    # 先去除标点
    text = remove(text)
    '''
    通过jieba进行分词并通过空格分隔,返回分词后的结果
    '''
    stopwords = stopwordslist('./stopwords.txt')
    jieba_word = jieba.cut(text, cut_all=False)  # cut_all是分词模式，True是全模式，False是精准模式，默认False
    data=[]
    for x in jieba_word:
        if x not in stopwords:
            data.append(x)
    seg_list = ' '.join(data)
    return seg_list
