#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/17 下午5:35
#   Desc    :   文章模块
import markdown2

from model import models
from app import BaseHandler, AdminHandler
from utilities import tool


class ShowArticlesHandler(BaseHandler):
    """
    展示文章列表
    """
    def get(self):
        articles_list = models.Article.find_by("""where status=0 order by create_time
                                               desc""")

        for fi_article in articles_list:
            fi_article['id'] = self._warp_id(fi_article['id'])
            user = models.User.find_first(
                'where uid=? and status=0', fi_article['uid'])
            fi_article['author'] = user

        self.render('article_list.html', articles_list=articles_list)
 

class ReadArticleHandler(BaseHandler):
    """
    阅读文章
    """
    def get(self, article_id):
        article_warp_id = article_id
        article_id = self._unwarp_id(article_id)
        article = models.Article.find_first('where id=? and status=0', article_id)
        article['article_warp_id'] = article_warp_id
        if article:
            ## TODO:不能刷！
            # 阅读数＋1
            article.read_times += 1
            article.update()

            # markdown转成html
            extras = ['tables', 'fenced-code-blocks']
            article.content = unicode(
                markdown2.markdown(
                    article.content,
                    extras=extras,
                    safe_mode='escape'
                )
            )
            article.author = models.User.find_first(
                'where uid=? and status=0', article.uid)
            # 对文章内容中的单词增加样式
            article.content = tool.make_content(article.content)
            self.render('article.html', **article)
        else:
            self.write_fail(message=u'文章不存在')


class PostArticleHandler(AdminHandler):
    """
    发布文章(现只有管理员可以发布文章）
    """
    def get(self):
        self.render('article_edit.html', title=u'发布文章', article={})

    def post(self):
        uid = self.get_user['uid']
        title = self.get_argument('title')
        zh_title = self.get_argument('zh_title')
        source_url = self.get_argument('source_url')
        content = self.get_argument('content')
        update_time = self.now()
        create_time = self.now()
        article = models.Article(
            uid=uid, title=title, zh_title=zh_title, content=content,
            source_url=source_url, create_time=create_time, update_time=update_time
        )
        article.insert()
        self.write_success()


class EditArticleHandler(AdminHandler):
    """
    编辑文章（只有管理原可以编辑文章）
    """
    def get(self, article_id):
        article_id = self._unwarp_id(article_id)
        article = models.Article.find_first(
            'where id=? and status=0', article_id)
        if article:
            self.render('article_edit.html', title=u'编辑文章', article=article)
        else:
            self.write_fail(message=u'文章不存在')