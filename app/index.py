#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/11 下午3:54
#   Desc    :   首页
from app import BaseHandler
from model import models


class MainHandler(BaseHandler):
    def get(self):
        static_url = {'demo1': '/static/tornado/index.html',
                      'demo2': '/static/image/fun.png'}
        self.render('home.html', **static_url)

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = models.User.find_first('where email=? and password=?',
                                      email, password)
        if user:
            self.session = {'uid': user.uid,
                            'nickname': user.nickname}
            self.redirect('/')
        else:
            self.render('status.html', message=u'登陆失败！')