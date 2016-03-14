#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/11 下午3:54
#   Desc    :   启动入口
import logging

from tornado import ioloop
from tornado.web import StaticFileHandler
from tornado.web import Application

from model import db
from config import configs
from app.chat_room import LoginHandler, TalkHandler, MessageHandler
from app.index import MainHandler
from app import login

# 设置logging级别
logging.basicConfig(level=logging.INFO)

# 链接数据库
db.create_engine(**configs['db'])

def make_app():
    return Application([
        (r'/', MainHandler),
        (r'/talk', TalkHandler),
        (r'/login', LoginHandler),
        (r'/message', MessageHandler),
        (r'/test_login', login.TestLoginHandler),
        (r'/sign', login.SignInHandler)
    ], StaticFileHandler, **configs['tornado_setting'])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)

    ioloop.IOLoop.current().start()
