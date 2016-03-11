#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/11 下午3:54
#   Desc    :   配置文件
import os


configs = {
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'test',
        'password': '521521',
        'database': 'test'
    },
    'tornado_setting':{
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'template_path': os.path.join(os.path.dirname(__file__), 'template'),
        'debug': True
    },
    'session': {
        'secret': 'XuEwEiHaN'
    }
}