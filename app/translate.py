#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/24 下午12:43
#   Desc    :   请求有道翻译api实现翻译功能
import json
import logging

from tornado.httpclient import HTTPClient, HTTPError
from tornado import log

from app import BaseHandler
from config import YouDao_API

_FORMAT = '?keyfrom={keyfrom}&key={key}&type=data&doctype=json&version=1.1&q=%s'


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
        if not keyword:
            self.write_fail('没有参数')
        youdao = YouDao(YouDao_API)
        data = youdao.get_translation(keyword)

        data = json.loads(data)

        # 检查是否是参数错误
        if data['errorCode']:
            logging.info('使用‘有道’翻译，参数传递错误！')
            return None

if __name__ == "__main__":
    log.enable_pretty_logging()