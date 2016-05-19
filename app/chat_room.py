#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/11 下午3:54
#   Desc    :   聊天室
from tornado.web import RequestHandler

MSG = {}

# class LoginHandler(RequestHandler):
#     def get(self):
#         self.render('login.html')
#
#     def post(self):
#         username = self.get_argument('username')
#         self.set_cookie('username', username)
#         self.redirect('/talk')


class TalkHandler(RequestHandler):
    def get(self):
        if not self.get_cookie('username'):
            self.redirect('/login')
        else:
            username = self.get_cookie('username')
            welcome = u"""欢迎%s来到聊天室""" % username.decode('utf-8')
            self.render('talk.html', **{'welcome': welcome})

    def post(self):
        username = self.get_cookie('username')
        message = u'%s 说:%s' % (username.decode('utf-8'), self.get_argument('message'))
        MSG[username] = message
        self.write(message)


class MessageHandler(RequestHandler):
    def get(self):
        if MSG:
            if self.get_cookie('username') not in MSG.keys():
                self.write(MSG.values()[0])
                MSG.clear()

