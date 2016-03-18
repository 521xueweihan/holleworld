#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/17 下午2:26
#   Desc    :   Handler的基类
import hashids
import json

from tornado.web import RequestHandler

from config import SALT


class BaseHandler(RequestHandler):
    """ 暂时主要功能是id加盐和用户状态的管理
    """
    _SESSION_COOKIE_KEY = "__SESSION__"

    def prepare(self):
        if self.request.path in ['/sign']:
            return
        elif (self.request.path not in ['/']) and (not self.session):
            self.redirect('/')
        elif self.session:
            self.current_user = self.get_user

    @property
    def __hashids(self):
        return hashids.Hashids(SALT, min_length=16,
                               alphabet='abcdefghijklmnopqrstuvwxyz1234567890')

    def _warp_id(self, _id):
        return self.__hashids.encode(_id)

    def _unwrap_id(self, warp_id):
        return self.__hashids.decode(warp_id)[0]

    @property
    def get_user(self):
        return json.loads(self.session)

    @property
    def session(self):
        return self.get_secure_cookie(self._SESSION_COOKIE_KEY)

    @session.setter
    def session(self, value):
        if isinstance(value, dict):
            value = json.dumps(value)
        self.set_secure_cookie(self._SESSION_COOKIE_KEY, value)

    @session.deleter
    def session(self):
        self.clear_cookie(self._SESSION_COOKIE_KEY)