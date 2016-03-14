#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/14 下午5:37
#   Desc    :   登陆
from model import models

from tornado.web import RequestHandler

class TestLoginHandler(RequestHandler):
    def get(self):
        self.render('test_login.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = models.User.find_first('where email=?', email)
        if user is None:
            self.write_error(333)


class SignInHandler(RequestHandler):
    def get(self):
        ## TODO 验证session中的用户状态
        self.render('sign_in.html')

    def post(self):
        email=self.get_argument('email')
        password = self.get_argument('password')
        nickname = self.get_argument('nickname')
        u = models.User(uid=123345, email=email, nickname=nickname, password=password)
        u.insert()
        self.write(u'200')