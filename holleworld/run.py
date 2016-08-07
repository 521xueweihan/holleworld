#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/11 下午3:54
#   Desc    :   启动入口
from tornado import ioloop
from tornado.web import StaticFileHandler
from tornado.web import Application
from tornado.options import define
from tornado.log import enable_pretty_logging

from model import db
from config import configs, PORTS, DEBUG
from app import index, article, translate, share, profile

# 设置logging级别
define("debugging", default=DEBUG, type=bool, help="Toggle debugging mode")
enable_pretty_logging()

# 链接数据库
db.create_engine(**configs['db'])


def make_app():
    return Application([
        (r'/', index.LoginHandler),
        (r'/sign', index.SignHandler),
        (r'/check/sign/name', index.CheckoutNameHandler),
        (r'/check/sign/email', index.CheckoutEmailHandler),
        (r'/logout', index.LogoutHandler),
        (r'/user/(\w+)', profile.ProfileHandler),
        (r'/article/list', article.ShowArticlesHandler),
        (r'/article/read/(\S+)', article.ReadArticleHandler),
        (r'/article/post', article.PostArticleHandler),
        (r'/article/edit/(\S+)', article.EditArticleHandler),
        (r'/article/delete/(\S+)', article.DeleteArticleHandler),
        (r'/translate', translate.TranslateHandler),
        # 暂不实现分享功能
        # (r'/share', share.ShareHandler),
        # (r'/share/praise', share.PraiseHandler),
    ], StaticFileHandler, **configs['tornado_setting'])

if __name__ == "__main__":
    app = make_app()
    app.listen(PORTS)
    print u"服务启动在端口：%s，一切流畅的飞起来了！ " % PORTS
    ioloop.IOLoop.instance().start()
