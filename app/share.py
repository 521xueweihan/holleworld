#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/4/10 下午2:24
#   Desc    :   分享好文模块
from app import BaseHandler
from model import models
from utilities import tool


class ShareHandler(BaseHandler):
    def get(self):
        share_list = models.Share.find_all()
        self.render('share.html', share_list=share_list)

    def post(self):
        zh_title = self.get_argument('zh_title', None)
        en_title = self.get_argument('en_title', None)
        url = self.get_argument('url', None)
        url = tool.re_url(url)
        if url:
            share = models.Share(zh_title=zh_title, en_title=en_title, url=url,
                                 creat_time=self.now(), uid=self.get_user['uid'])
            share.insert()
            self.render('status.html', message='ok!')
        else:
            self.write_fail(message=u'参数错误')
