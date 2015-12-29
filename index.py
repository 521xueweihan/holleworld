# coding: utf-8
"""
__title__   =  '雪B最NB'
__mtime__   =  '15/12/29'
__author__  =  'XueWeihan'

"""
import os

import tornado.ioloop
import tornado.web


SETTINGS = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'template'),
    'debug': True
}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        static_url = {'demo1': '/static/tornado/index.html',
                      'demo2': '/static/image/fun.png'}
        self.render('home.html', **static_url)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ], tornado.web.StaticFileHandler, **SETTINGS)

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
