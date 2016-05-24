#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/4/5 下午10:56
#   Desc    :   一些工具方法
import re


def insert_span(words_list):
    """
    对内容进行处理，对单词加入样式类，用于单词变色
    """
    for i, fi_word in enumerate(words_list):
        _re = re.compile(r'^[A-Za-z]+$')
        re_result = _re.match(fi_word)
        if re_result:
            words_list[i] = '<span class=word-' + re_result.group().lower() + \
                            '>' + fi_word + '</span>'
        return ' '.join(words_list)


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
