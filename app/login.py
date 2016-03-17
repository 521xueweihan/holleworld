#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/14 下午5:37
#   Desc    :   登陆
from model import models
from app import BaseHandler





class LogoutHandler(BaseHandler):
    """ 注销
    """
    def get(self):
        del self.session
        self.redirect('/')


class RegisterHandler(BaseHandler):
    """
    注册
    """
    def get(self):
        if self.session:
            self.render('status.html', message=u'已处于登陆状态')
        self.render('register.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        nickname = self.get_argument('nickname')
        u = models.User(email=email, nickname=nickname, password=password)
        try:
            u.insert()
        except Exception as e:
            self.render('status.html', message=u'注册失败！')


        self.render('status.html', message=u'注册成功！')