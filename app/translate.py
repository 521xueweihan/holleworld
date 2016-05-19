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

from model import models
from app import BaseHandler
from config import YouDao_Key

_FORMAT = '?keyfrom={keyfrom}&key={key}&type=data&doctype=json&version=1.1&q=%s'

YouDao_ERROR = {
    20: '要翻译的文本过长',
    30: '无法进行有效的翻译',
    40: '不支持的语言类型',
    50: '无效的key',
    60: '无词典结果，仅在获取词典结果生效'}


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
            logging.info('使用‘有道’，翻译：%s' % q)
            response = HTTPClient().fetch(self.api % q)
        except Exception:
            logging.error('翻译：{}，出错！'.format(q))
            return None
        data = response.body
        return data


def save_word(uid, query_word, data):
    """
    把查询的单词存到数据库中，如果数据库已经有了就把查询次数＋1
    :param uid: 用户id
    :param query_word: 查询的单词
    """
    word = models.Words.find_first('where uid=? and word=?', uid, query_word)
    if word:
        word = models.Words.get(word.id)
        word.count += 1
        word.update_time = datetime.datetime.now()
        word.update()
        logging.info('{}查询次数＋1'.format(query_word))
        data['count'] = word.count
        return

    models.Words(uid=uid, word=query_word,
                 create_time=datetime.datetime.now()).insert()
    data['count'] = 1
    logging.info("存储单词:{},成功！".format(query_word))


class TranslateHandler(BaseHandler):
    def get(self):
        keyword = self.get_argument('keyword', None)
        if not keyword:
            self.write_fail(message=u'没有参数！')

        youdao = YouDao(**YouDao_Key)
        data = youdao.translation(keyword)

        if data is None:
            return self.write_fail(message=u'选择的翻译内容错误！')

        data = json.loads(data)

        # 检查是否参数错误
        if data['errorCode'] in YouDao_ERROR.keys():
            logging.info('{}！'.format(YouDao_ERROR[data['errorCode']]))
            return self.write_fail(message=YouDao_ERROR[data['errorCode']])

        # 只存储单词，不存储词组等其他形式
        if 'basic' in data.keys():
            if self.get_user:
                save_word(self.get_user['uid'], keyword, data)
            else:
                # 未登录状态下，uid为0
                save_word(0, keyword, data)

        return self.write_success(data)

if __name__ == "__main__":
    log.enable_pretty_logging()