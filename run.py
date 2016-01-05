# coding: utf-8
"""
__title__   =  '雪B最NB'
__mtime__   =  '16/1/5'
__author__  =  'XueWeihan'

"""
import os
from tornado import ioloop
from tornado.web import StaticFileHandler
from tornado.web import Application

from app.chat_room import LoginHandler, TalkHandler, MessageHandler
from app.index import MainHandler

SETTINGS = {
    # 暂时先这样，我觉得有更好的方法！
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'template'),
    'debug': True
}


def make_app():
    return Application([
        (r'/', MainHandler),
        (r'/talk', TalkHandler),
        (r'/login', LoginHandler),
        (r'/message', MessageHandler)
    ], StaticFileHandler, **SETTINGS)

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)

    ioloop.IOLoop.current().start()
