#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/14 下午5:37
#   Desc    :   登陆
from tornado.web import RequestHandler

from model import db, models


class LoginHandler(RequestHandler):
    """
    登陆
    """
    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = models.User.find_first('where email=?', email)
        if user.password == password:
            self.render('status.html', message=u'登陆成功！')
        else:
            self.render('status.html', message=u'登陆失败！')


class RegisterHandler(RequestHandler):
    """
    注册
    """
    def get(self):
        ## TODO 验证session中的用户状态
        self.render('register.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        nickname = self.get_argument('nickname')
        u = models.User(email=email, nickname=nickname, password=password)
        try:
            u.insert()
        except:
            self.render('status.html', message=u'注册失败！')


        self.render('status.html', message=u'注册成功！')