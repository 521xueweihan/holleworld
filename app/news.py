#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/17 下午5:35
#   Desc    :   news模块
import datetime

import markdown2

from model import models
from app import BaseHandler


class NewsHandler(BaseHandler):
    """ 展示新闻
    """
    def get(self):
        news_list = models.News.find_all()
        for new in news_list:
            new.content = markdown2.markdown(new.content)
        self.render('news.html', news_list=news_list)


class NewsEditHandler(BaseHandler):
    """ 发布新闻
    """
    def get(self):
        self.render('news_edit.html')

    def post(self):
        if not self.get_user['admin']:
            self.render('status.html', message=u'对不起你没有权限！')
            return
        title = self.get_argument('title')
        content = self.get_argument('content')
        create_time = datetime.datetime.now()
        news = models.News(title=title, content=content, create_time=create_time)
        news.insert()
        self.render('status.html', message=u'发布新闻成功！')