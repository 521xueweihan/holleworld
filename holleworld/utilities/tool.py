#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/4/5 下午10:56
#   Desc    :   一些工具方法
import re

from bs4 import BeautifulSoup


def insert_class(soup, tag):
    """
    对单词加入样式类，用于单词变色
    """
    article_tag = soup.find_all(tag)
    for fi_tag in article_tag:
        if fi_tag:
            new_tag = soup.new_tag(tag)
            word_list = fi_tag.text.split(' ')
            for i, fi_word in enumerate(word_list):
                # 正则表达式匹配单词
                _re = re.compile(r'^[A-Za-z]+$')
                re_result = _re.match(fi_word)
                if re_result:
                    # 经匹配如果是单词则创建新的tag对象，同时加入class
                    new_word_tag = soup.new_tag('span')
                    new_word_tag['class'] = 'word-' + re_result.group().lower()
                    new_word_tag.string = fi_word+' '
                    new_tag.append(new_word_tag)
            if word_list and new_tag.text:
                # 替换成加了class的tag对象
                fi_tag.replace_with(new_tag)


def make_content(article_html):
    """
    对内容进行处理
    """
    soup = BeautifulSoup(article_html, 'html.parser')
    tags = ['p', 'li']
    for tag in tags:
        insert_class(soup, tag)
    return soup


def re_url(s):
    """
    利用正则匹配url
    符合->返回(不含参数：'?arg=xxx')的url
    不符合->返回None
    """
    if not s.startswith(('http', 'https')):
        s = 'http://' + s
    _re = re.compile(r'(http|https)+://[^\s?]*')
    re_result = _re.match(s)
    if re_result:
        return re_result.group()
    else:
        return ''


def my_to_sting(obj):
    """
    转化成str对象
    """
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    elif isinstance(obj, str):
        return obj.decode('utf-8').encode('utf-8')


def check_arg(arg):
    """
    检查用户名和邮箱的合法性
    """
    # 不安全的字符
    unsafe_char = ['<', '>', '&']
    if arg:
        for fi_unsafe_char in unsafe_char:
            if fi_unsafe_char in arg:
                return False
    else:
        return False
    return True