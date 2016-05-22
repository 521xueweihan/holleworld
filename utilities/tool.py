#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/4/5 下午10:56
#   Desc    :   一些工具方法
import re


def insert_span(s):
    """
    对内容进行处理
    """
    ## TODO 应应该用正则表达式否则内容中的'>'都会被删除

    # 不对img标签的内容进行处理
    if '<img>' in s:
        return s
    # 内容的每个单词都增加<span>标签，用于单词变色
    elif ('<' not in s) or ('>' not in s):
        return '<span class='+s+'>'+s+'</span>'
    #
    return ''


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
