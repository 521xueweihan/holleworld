#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/11 下午3:54
#   Desc    :   配置文件
import os

# debug模式
DEBUG = True

# 监听的端口
PORTS = 8000

# ROOT PATH
ROOT_PATH = os.path.dirname(__file__)

# 盐
SALT = '54xueweihan5zuiNB'

# 翻译key
YouDao_Key = {
    'key': 1589417428,
    'keyfrom': 'holleworld'
}

# 七牛
QiNiu_KEY = {
    'access_key': '',
    'secret_key': ''
}

configs = {
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'test',
        'password': '521521',
        'database': 'holleworld'
    },
    'tornado_setting':{
        'static_path': os.path.join(ROOT_PATH, 'static'),
        'template_path': os.path.join(ROOT_PATH, 'template'),
        'debug': True,
        'cookie_secret': 'XuEwEiHaN'
    },
    'session': {
        'secret': 'XuEwEiHaN'
    }
}