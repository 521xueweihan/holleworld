# coding: utf-8
"""
__title__   =  '雪B最NB'
__mtime__   =  '15/12/29'
__author__  =  'XueWeihan'

"""
import os

from tornado.web import RequestHandler

class MainHandler(RequestHandler):
    def get(self):
        static_url = {'demo1': '/static/tornado/index.html',
                      'demo2': '/static/image/fun.png'}
        self.render('home.html', **static_url)

