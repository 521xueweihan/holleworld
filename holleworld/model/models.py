#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/14 下午5:18
#   Desc    :   ORM对象

import db
from model.orm import Model, StringField, TimeField, IntegerField, TextField


class Code(Model):
    __table__ = 'code'

    id = IntegerField(primary_key=True, updatable=False, ddl='bigint(20)')
    code = StringField(ddl='varchar(50)')
    status = IntegerField(ddl='tinyint(4)', default=0)
    update_time = TimeField()
    create_time = TimeField()


class User(Model):
    __table__ = 'user'

    id = IntegerField(primary_key=True, updatable=False, ddl='bigint(20)')
    uid = IntegerField(default=db.next_id(), updatable=False, ddl='bigint(20)')
    email = StringField(ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(10)')
    avatar = StringField(ddl='varchar(500)')
    admin = IntegerField(ddl='tinyint(4)', default=0)
    create_time = TimeField()


class Article(Model):
    __table__ = 'article'

    id = IntegerField(primary_key=True, updatable=False, ddl='bigint(20)')
    author_id = IntegerField(updatable=False, ddl='bigint(20)')
    last_editor_id = IntegerField(updatable=True, ddl='bigint(20)')
    title = StringField(ddl='varchar(500)')
    zh_title = StringField(ddl='varchar(500)')
    source_url = StringField(ddl='varchar(500)')
    content = TextField()
    read_times = IntegerField(ddl='bigint(10)', default=0)
    point = IntegerField(ddl='bigint(10)', default=0)
    status = IntegerField(ddl='tinyint(4)', default=0)
    update_time = TimeField()
    create_time = TimeField()


class Words(Model):
    __table__ = 'words'

    id = IntegerField(primary_key=True, updatable=False, ddl='bigint(20)')
    uid = IntegerField(updatable=False, ddl='bigint(20)')
    count = IntegerField(ddl='bigint(20)', default=1)
    word = StringField(ddl='varchar(50)')
    update_time = TimeField()
    create_time = TimeField()


class Share(Model):
    __table__ = 'share'

    id = IntegerField(primary_key=True, updatable=False, ddl='bigint(20)')
    uid = IntegerField(updatable=False, ddl='bigint(20)')
    zh_title = StringField(ddl='varchar(50)')
    en_title = StringField(ddl='varchar(50)')
    url = StringField(ddl='varchar(50)')
    good = IntegerField(ddl='bigint(20)', default=0)
    update_time = TimeField()
    create_time = TimeField()


class Data(Model):
    """ 爬取的github内容 """
    __table__ = 'data'

    id = IntegerField(primary_key=True, updatable=False, ddl='bigint(20)')
    url = StringField(ddl='varchar(500)')
    content = TextField()
    update_time = TimeField()
    create_time = TimeField()


class Proxy(Model):
    """ 代理 """
    __table__ = 'proxy'

    id = IntegerField(primary_key=True, updatable=False, ddl='bigint(20)')
    proxy_host = StringField(ddl='varchar(500)')
    proxy_port = StringField(ddl='varchar(500)')
    create_time = TimeField()
