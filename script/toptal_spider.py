#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/31 下午4:21
#   Desc    :   爬取https://www.toptal.com/blog内容
import datetime

from bs4 import BeautifulSoup
from tornado import httpclient

from model import models, db
from config import configs
db.create_engine(**configs['db'])

TEST_URL = 'https://www.toptal.com/tornado/simple-python-websocket-server'


class Content(object):
    def __init__(self):
        self.url = None
        self.title = None
        self.content = None
        self.source = None

    def get_content(self):
        http_client = httpclient.HTTPClient()
        response = http_client.fetch(TEST_URL)
        self.content = response.body

    def clear_content(self):
        soup = BeautifulSoup(self.content, "html.parser")
        self.title = unicode(soup.find('h1', 'post_title-text').string)
        self.content = soup.find('div', 'content_body').prettify()

    def save(self):
        create_time = datetime.datetime.now()
        news = models.News(title=self.title, content=self.content, create_time=create_time)
        news.insert()

a = Content()
a.get_content()
a.clear_content()
a.save()