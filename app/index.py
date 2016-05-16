#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/11 下午3:54
#   Desc    :   首页
import logging

from app import BaseHandler, UserHandler
from model import models


class LoginHandler(UserHandler):
    """
    登陆
    """
    def get(self):
        # log记录访问者的ip
        logging.info('{}！'.format(self.request.remote_ip))
        if self.session:
            self.redirect('/article/list')
        self.render('index.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = models.User.find_first('where email=? and password=?',
                                      email, password)
        if user:
            self.session = {'uid': user.uid,
                            'nickname': user.nickname,
                            'admin': user.admin}
            self.write_success()
        else:
            self.write_fail()


class SignHandler(UserHandler):
    """
    注册
    """
    def get(self):
        self.render('register.html')

    def post(self):
        ## TODO 已经注册过的邮箱不能重复注册
        email = self.get_argument('email')
        password = self.get_argument('password')
        nickname = self.get_argument('nickname')
        u = models.User(email=email, nickname=nickname, password=password)
        try:
            u.insert()
        except Exception:
            self.render('status.html', message=u'注册失败！')

        self.render('status.html', message=u'注册成功！')


class LogoutHandler(UserHandler):
    """
    注销
    """
    def get(self):
        del self.session
        self.redirect('/')


class TestHandler(BaseHandler):
    """
    用于练习一些功能
    """
    def get(self):
        # self.render('upload_pic.html')
        self.render('test.html')

    def post(self):
        img_file = self.request.fi

        print img_file
