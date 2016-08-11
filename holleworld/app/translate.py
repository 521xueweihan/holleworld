#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/24 下午12:43
#   Desc    :   请求有道翻译api实现翻译功能
import json
import logging
import datetime

from tornado.httpclient import HTTPClient
from tornado import log

from model.models import Words
from app import BaseHandler
from utilities import tool
from config import YouDao_Key


_FORMAT = '?keyfrom={keyfrom}&key={key}&type=data&doctype=json&version=1.1&q=%s'

YouDao_ERROR = {
    20: u'要翻译的文本过长',
    30: u'无法进行有效的翻译',
    40: u'不支持的语言类型',
    50: u'无效的key',
    60: u'无词典结果，仅在获取词典结果生效'}


class YouDao(object):
    def __init__(self, keyfrom, key):
        self.url = 'http://fanyi.youdao.com/openapi.do'
        self.keyfrom = keyfrom
        self.key = key

    @property
    def api(self):
        return self.url+_FORMAT.format(keyfrom=self.keyfrom, key=self.key)

    def translation(self, q):
        try:
            logging.info('使用‘有道’，翻译：{}'.format(tool.my_to_sting(q)))
            response = HTTPClient().fetch(self.api % q)

        except Exception:
            logging.error('翻译：{}，出错'.format(tool.my_to_sting(q)))
            return None
        data = response.body
        return data


def save_word(uid, query_word, data):
    """
    把查询的单词存到数据库中：
    如果数据库已经有了就把查询次数＋1
    如果原来没有查过，就count初始化为 1
    :param uid: 用户id
    :param data: 请求翻译api，返回的结果（无count字段）
    :param query_word: 查询的单词
    """
    # 未登录的用户，不记录查询次数
    word = Words.find_first('where uid=? and word=?', uid, query_word)
    if word:
        word = Words.get(word.id)
        word.count += 1
        word.update_time = datetime.datetime.now()
        word.update()
        data['count'] = word.count
        logging.info('{},查询次数＋1'.format(tool.my_to_sting(query_word)))
    else:
        # 初始化count为 1
        data['count'] = 1
        Words(uid=uid, word=query_word,
                     create_time=datetime.datetime.now()).insert()
    logging.info("存储单词:{},成功！".format(tool.my_to_sting(query_word)))


class TranslateHandler(BaseHandler):
    def post(self):
        keyword = self.get_argument('keyword', None)
        keyword = keyword.lower()
        if not keyword:
            self.write_fail(message=u'没有参数')

        youdao = YouDao(**YouDao_Key)
        data = youdao.translation(keyword)

        if data is None:
            self.write_fail(message=u'选择的翻译内容错误')

        data = json.loads(data)

        # 检查是否参数错误
        if data['errorCode']:
            self.write_fail(message=YouDao_ERROR[data['errorCode']])

        # 只存储单词，不存储词组等其他形式
        if 'basic' in data.keys():
            if self.get_user:
                # 只有当用户登录的后，才记录查询单词的次数
                save_word(self.get_user['uid'], keyword, data)
        else:
            # 没有basic key则代表：没有翻译成功（不翻译句子的情况考虑）
            self.write_fail(message=u'查无此词')
        self.write_success(data)

if __name__ == "__main__":
    log.enable_pretty_logging()