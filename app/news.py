#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/17 下午5:35
#   Desc    :   news模块
import datetime
import re

import markdown2

from model import models
from app import BaseHandler
from utilities import escape, tool


class NewsHandler(BaseHandler):
    """ 展示新闻列表
    """
    def get(self):
        news_list = models.News.find_all()
        for fi_new in news_list:
            fi_new['id'] = self._warp_id(fi_new['id'])
        self.render('show_article.html', news_list=news_list)


class NewHandler(BaseHandler):
    """
    展示新闻
    """
    def get(self, article_id):
        article_id = self._unwarp_id(article_id)
        new = models.News.find_first('where id=?', article_id)
        # markdown转成html
        new.content = unicode(markdown2.markdown(new.content, extras=['tables',
                                                                      'fenced-code-blocks']))
        self.render('article.html', **new)


class NewsEditHandler(BaseHandler):
    """ 发布新闻
    """
    def get(self):
        self.render('news_edit.html')

    def post(self):
        if not self.get_user['admin']:
            self.render('status.html', message=u'对不起你没有权限！')
            return

        title = self.get_argument('title')
        content = self.get_argument('content')

        # new_content = []
        #
        # 反转义代码块中的"&amp;"
        # m = re.compile('\<pre\>[\s\S]*\<\/pre\>')
        # content = m.sub(escape.code_unescape, content)
        #
        # for span_content in content.split(' '):
        #     new_content.append(tool.insert_span(span_content))
        #
        # content = ' '.join(new_content)

        create_time = datetime.datetime.now()

        news = models.News(title=title, content=content, create_time=create_time)
        news.insert()
        self.render('status.html', message=u'发布新闻成功！')