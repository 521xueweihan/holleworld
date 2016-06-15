#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/6/12 下午3:14
#   Desc    :   个人页面
from app import UserHandler
from model import models

# pylint: disable=W0221


class ProfileHandler(UserHandler):
    def get(self, uid):
        user = models.User.find_first('where uid=? and status=0', uid)
        self.render('profile.html', user=user)
