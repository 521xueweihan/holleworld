#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/14 下午5:18
#   Desc    :   ORM对象

import datetime
import time
import uuid

from db import next_id
from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField


class User(Model):
    __table__ = 'user'

    id = IntegerField(primary_key=True, ddl='bigint(20)')
    uid = IntegerField(default=next_id, ddl='bigint(20)')
    email = StringField(ddl='varchar(20)')
    nickname = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(6)')