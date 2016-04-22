#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/31 下午4:21
#   Desc    :   爬虫
import datetime

from bs4 import BeautifulSoup
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPClient

from model import models, db
from config import configs
from client_config import CLIENT_CONFIG
db.create_engine(**configs['db'])

TEST_URL = 'https://api.github.com/search/users?q=tom'


class Spider(object):
    """
    爬取
    """
    def __init__(self, url, **kwargs):
        self.request = HTTPRequest(url, **dict(CLIENT_CONFIG, **kwargs))

    def get(self):
        return HTTPClient().fetch(self.request)

    def post(self):
        self.request.method = "POST"
        return HTTPClient().fetch(self.request)


class Content(object):
    """
    存储内容到数据库
    """
    def __init__(self):
        self.url = None
        self.content = None

    def get_content(self, url, content):
        self.url = url
        self.content = content

    def save(self):
        create_time = datetime.datetime.now()
        data = models.Data(url=self.url, content=self.content, create_time=create_time)
        data.insert()

s = Spider(TEST_URL)
response = s.get()
t = Content()

import json
return_json = json.loads(response.body)
for item in return_json['items']:
    t.get_content(item['html_url'], item['login'])
    t.save()