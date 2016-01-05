# coding: utf-8
"""
__title__   =  '雪B最NB'
__mtime__   =  '15/12/29'
__author__  =  'XueWeihan'

"""
import os

from tornado import ioloop
from tornado.web import StaticFileHandler
from tornado.web import RequestHandler, Application
from tornado.options import define, options

from app.chat_room import LoginHandler, TalkHandler, MessageHandler

SETTINGS = {
    # 暂时先这样，我觉得有更好的方法！
    'static_path': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
    'template_path': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'template'),
    'debug': True
}


class MainHandler(RequestHandler):
    def get(self):
        static_url = {'demo1': '/static/tornado/index.html',
                      'demo2': '/static/image/fun.png'}
        self.render('home.html', **static_url)

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
    options.logging = "debug"

    ioloop.IOLoop.current().start()
