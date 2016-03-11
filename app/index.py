#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/11 下午3:54
#   Desc    :   首页
from tornado.web import RequestHandler

class MainHandler(RequestHandler):
    def get(self):
        static_url = {'demo1': '/static/tornado/index.html',
                      'demo2': '/static/image/fun.png'}
        self.render('home.html', **static_url)

