#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/11 下午3:54
#   Desc    :   首页
import logging

from app import BaseHandler
from model import models


class MainHandler(BaseHandler):
    def get(self):
        # 显示访问者的ip
        # logging.info('{}！'.format(self.request.remote_ip))
        self.render('new_index.html')
        # static_url = {'demo1': '/test',
        #               'demo2': '/share',
        #               'demo3': '/news'}
        # self.render('home.html', **static_url)

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


class TestHandler(BaseHandler):
    def get(self):
        self.render('upload_pic.html')

    def post(self):
        img_file = self.request.fi

        print img_file


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