#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/17 下午2:26
#   Desc    :   Handler的基类
import hashids
import json
import datetime
import decimal

from tornado.web import RequestHandler, Finish

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
    def now(self):
        """
        返回当前时间方法
        :return:方法
        """
        return datetime.datetime.now

    @property
    def __hashids(self):
        """
        返回Hashids对象
        """
        return hashids.Hashids(SALT, min_length=16,
                               alphabet='abcdefghijklmnopqrstuvwxyz1234567890')

    def _warp_id(self, _id):
        """
        加密id
        :param _id:真实的id
        :return:加盐的id
        """
        return self.__hashids.encode(_id)

    def _unwrap_id(self, warp_id):
        """
        解密id
        :param warp_id:加密的id
        :return:真实的id
        """
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

    def conv_valid_json(self, data):
        """ 将一些数据改为合法的 JSON, 比如 日期
        """
        if isinstance(data, dict):
            for key in data:
                data[key] = self.conv_valid_json(data[key])

        if isinstance(data, (list, tuple)):
            data = [self.conv_valid_json(x) for x in data]

        if isinstance(data, datetime.datetime):
            data = data.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(data, datetime.date):
            data = data.strftime("%Y-%m-%d")

        if isinstance(data, decimal.Decimal):
            data = str(data)

        return data

    def write_success(self, data=None):
        self.write({"success": True, "code": 200, "data": self.conv_valid_json(data)})

    def write_fail(self, **extra):
        """ 抛出结束异常来确保代码不会继续执行 """
        extra.update({"success": False})
        self.write(extra)
        raise Finish  # 确保代码不会在返回错误后继续执行