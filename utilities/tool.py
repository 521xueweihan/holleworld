#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/4/5 下午10:56
#   Desc    :   一些工具方法
import re

from bs4 import BeautifulSoup


def insert_span(article_html):
    """
    对内容进行处理，对单词加入样式类，用于单词变色
    """
    soup = BeautifulSoup(article_html, 'html.parser')
    article_p = soup.find_all('p')
    for fi_p in article_p:
        if fi_p:
            new_tag = soup.new_tag('p')
            word_list = fi_p.text.split(' ')
            for i, fi_word in enumerate(word_list):
                _re = re.compile(r'^[A-Za-z]+$')
                re_result = _re.match(fi_word)
                if re_result:
                    new_word_tag = soup.new_tag('span')
                    new_word_tag['class'] = 'word-' + re_result.group().lower()
                    new_word_tag.string = fi_word+' '
                    new_tag.append(new_word_tag)
            if word_list and new_tag.string:
                fi_p.replace_with(new_tag)
    return soup


def re_url(s):
    """
    利用正则匹配url
    符合->返回(不含参数：'?arg=xxx')的url
    不符合->返回None
    """
    _re = re.compile(r'(http|https)+://[^\s?]*')
    re_result = _re.match(s)
    if re_result:
        return re_result.group()
    else:
        return None


def my_to_sting(obj):
    """
    转化成str对象
    """
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    elif isinstance(obj, str):
        return obj.decode('utf-8').encode('utf-8')
