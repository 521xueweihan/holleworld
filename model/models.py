#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/14 下午5:18
#   Desc    :   ORM对象

from db import next_id
from orm import Model, StringField, TimeField, IntegerField, TextField


class User(Model):
    __table__ = 'user'

    id = IntegerField(primary_key=True, updatable=False, ddl='bigint(20)')
    uid = IntegerField(default=next_id(), updatable=False, ddl='bigint(20)')
    email = StringField(ddl='varchar(50)')
    nickname = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(6)')
    admin = IntegerField(ddl='tinyint')
    create_time = TimeField()


class News(Model):
    __table__ = 'news'

    id = IntegerField(primary_key=True, updatable=False, ddl='bigint(20)')
    title = StringField(ddl='varchar(500)')
    content = TextField()
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
    __table__ = 'data'

    id = IntegerField(primary_key=True, updatable=False, ddl='bigint(20)')
    url = StringField(ddl='varchar(500)')
    content = TextField()
    update_time = TimeField()
    create_time = TimeField()