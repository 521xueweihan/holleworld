#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/24 下午12:43
#   Desc    :   请求有道翻译api实现翻译功能
import json
import logging

from tornado.httpclient import HTTPClient
from tornado import log

from app import BaseHandler
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

    def get_translation(self, q):
        try:
            logging.info('使用‘有道’，翻译：{}'.format(q))
            response = HTTPClient().fetch(self.api % q)
        except Exception:
            logging.error('翻译：{}，网络出错！'.format(q))
            return None
        data = response.body
        return data


class TranslateHandler(BaseHandler):
    def get(self):
        keyword = self.get_argument('keyword', None)
        print keyword
        if not keyword:
            self.write_fail(message=u'没有参数')
        youdao = YouDao(**YouDao_Key)
        data = youdao.get_translation(keyword)

        data = json.loads(data)

        # 检查是否参数错误
        if data['errorCode'] in YouDao_Key.keys():
            logging.info('使用‘有道’翻译，{}！'.format(YouDao_Key[data['errorCode']]))
            return None
        return self.write_success(data)

if __name__ == "__main__":
    log.enable_pretty_logging()