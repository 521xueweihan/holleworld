#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/17 下午5:35
#   Desc    :   文章模块
import markdown2

from model.models import Article, User
from app import BaseHandler, AdminHandler
from utilities import tool


class ShowArticlesHandler(BaseHandler):
    """
    展示文章列表
    """
    def get(self):
        # 一页二十条
        page = int(self.get_argument('page', 1))
        total = Article.count_by('where status=0')
        articles_list = Article.find_by(
            """where status=0 order by create_time desc limit ?, ?""",
            (page-1)*20, page*20
        )
        has_more = total > page*20
        for fi_article in articles_list:
            fi_article['id'] = self._warp_id(fi_article['id'])
            user = User.find_first(
                'where uid=? and status=0', fi_article['author_id']
            )
            fi_article['author'] = user
            fi_article['show_source_url'] = fi_article.source_url.split('://')[1]
            # 原文地址只展示host
            fi_article['show_source_url'] = fi_article['show_source_url'].split('/')[0]
        self.render('article_list.html', articles_list=articles_list,
                    has_more=has_more, page=page)
 

class ReadArticleHandler(BaseHandler):
    """
    阅读文章
    """
    def get(self, article_id):
        article_warp_id = article_id
        article_id = self._unwarp_id(article_id)
        article = Article.find_first('where id=? and status=0', article_id)
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
            article.author = User.find_first(
                'where uid=? and status=0', article.author_id)
            # 对文章内容中的单词增加样式
            article.content = tool.make_content(article.content)
            # 判断权限是否有编辑以及删除功能
            # 作者以及管理员有编辑权限
            user_power = self.get_user.get('admin', None)
            if user_power == 1 and \
               self.get_user.get('uid') == article.author_id:
                article.can_edit = True
            elif self.get_user.get('admin', None) > 1:
                article.can_edit = True
            else:
                article.can_edit = False
            self.render('article.html', **article)
        else:
            self.write_fail(message=u'文章不存在')


class PostArticleHandler(AdminHandler):
    """
    发布文章
    """
    def get(self):
        self.render(
            'article_edit.html', title=u'发布文章', path='/article/post',
            article=None)

    def post(self):
        author_id = self.get_user['uid']
        last_editor_id = self.get_user['uid']
        title = self.get_argument('title')
        zh_title = self.get_argument('zh_title')
        source_url = tool.re_url(self.get_argument('source_url'))
        content = self.get_argument('content')
        update_time = self.now()
        create_time = self.now()
        article = Article(
            author_id=author_id, last_editor_id=last_editor_id, title=title,
            zh_title=zh_title, content=content, source_url=source_url,
            create_time=create_time, update_time=update_time
        )
        article.insert()
        self.write_success()


class EditArticleHandler(AdminHandler):
    """
    编辑文章
    """
    def get(self, article_id):
        article_warp_id = article_id
        article_id = self._unwarp_id(article_id)
        article = Article.find_first(
            'where id=? and status=0', article_id)
        if article:
            data = {
                'title': u'编辑文章',
                'article': article,
                'path': '/article/edit/' + article_warp_id
            }
            self.render('article_edit.html', **data)
        else:
            self.write_fail(message=u'文章不存在')

    def post(self, article_id):
        last_editor_id = self.get_user.get('uid', None)
        title = self.get_argument('title', None)
        zh_title = self.get_argument('zh_title', None)
        source_url = tool.re_url(self.get_argument('source_url', None))
        content = self.get_argument('content', None)
        update_time = self.now()
        article_id = self._unwarp_id(article_id)
        article = Article.find_first('where id=? and status=0', article_id)
        if not article:
            self.write_fail(message=u'文章不存在')
        elif article.author_id == self.get_user.get('uid') \
            or self.get_user.get('admin', 0) > 1:
            article.last_editor_id = last_editor_id
            article.title = title
            article.zh_title = zh_title
            article.source_url = source_url
            article.content = content
            article.update_time = update_time
            article.update()
            self.write_success()
        else:
            self.write_fail(message=u'没有权限')


class DeleteArticleHandler(AdminHandler):
    """
    删除文章
    """
    def post(self, article_id):
        article_id = self._unwarp_id(article_id)
        article = Article.find_first('where id=? and status=0', article_id)
        if not article:
            self.write_fail(message=u'文章不存在')
        elif article.author_id == self.get_user.get('uid') \
             or self.get_user.get('admin', 0) > 1:
            article.status = 1
            article.update()
            self.write_success()
        else:
            self.write_fail(message=u'没有权限')