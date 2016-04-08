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
                      'demo2': '/news',
                      'demo3': '/static/test_react/index.html'}
        self.render('home.html', **static_url)

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = models.User.find_first('where email=? and password=?',
                                      email, password)
        if user:
            self.session = {'uid': user.uid,
                            'nickname': user.nickname,
                            'admin': user.admin}
            self.redirect('/')
        else:
            self.render('status.html', message=u'登陆失败！')


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
        ## TODO 已经注册过的邮箱不能重复注册
        email = self.get_argument('email')
        password = self.get_argument('password')
        nickname = self.get_argument('nickname')
        u = models.User(email=email, nickname=nickname, password=password)
        try:
            u.insert()
        except Exception as e:
            self.render('status.html', message=u'注册失败！')


        self.render('status.html', message=u'注册成功！')