#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/6/9 下午5:04
#   Desc    :   上传图片
import os
import logging

from qiniu import Auth, put_file, put_data

from config import QiNiu_KEY, ROOT_PATH

LOCAL_IMG_PATH = 'uploads'

PUBLIC_URL = '7xv88n.com1.z0.glb.clouddn.com/'


class QiNiu(object):
    #需要填写你的 Access Key 和 Secret Key
    access_key = QiNiu_KEY['access_key']
    secret_key = QiNiu_KEY['secret_key']

    def __init__(self, file_name, bucket_name='holleworld-img'):
        # 要上传的空间
        self.bucket_name = bucket_name
        # 上传到七牛后保存的文件名
        self.key = file_name
        # 要上传文件的本地路径
        self.localfile = os.path.join(ROOT_PATH, LOCAL_IMG_PATH, file_name)

    @property
    def token(self):
        # 构建鉴权对象
        q = Auth(QiNiu.access_key, QiNiu.secret_key)
        # 生成上传 Token，可以指定过期时间等
        _token = q.upload_token(self.bucket_name, self.key, 3600)
        return _token

    def upload_file(self):
        """
        上传文件
        """
        ret, info = put_file(self.token, self.key, self.localfile)
        if info.status_code == 200:
            return PUBLIC_URL+ret.get('key', None)
        else:
            logging.error(info.status_code)
            return None

    def upload_data(self, data):
        """
        上传二进制字符串
        """
        ret, info = put_data(self.token, self.key, data)
        if info.status_code == 200:
            return PUBLIC_URL+ret.get('key', None)
        else:
            logging.error(info)
            return None

if __name__ == '__main__':
    qiniu_obj = QiNiu('holleworld-img', '341d4760-3d0e-4e3e-b340-6048ecf7e04b.jpg')
    print qiniu_obj.upload_file()