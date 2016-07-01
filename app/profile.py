#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/6/12 下午3:14
#   Desc    :   个人页面
import os
import uuid

from app import UserHandler
from model import models
from utilities import qiniu_upload_img


class ProfileHandler(UserHandler):
    def get(self, uid):
        user = models.User.find_first('where uid=? and status=0', uid)
        self.render('profile.html', user=user, uid=uid)

    def post(self, uid):
        """
        更新用户信息（暂时只做了上传头像）
        """
        user = models.User.find_first('where uid=? and status=0', uid)
        if not user:
            self.write_fail(message=u'用户不存在')
        img_info = self.request.files['filearg'][0]
        img_name = img_info['filename']
        extn = os.path.splitext(img_name)[1]
        img_name = str(uuid.uuid4()) + extn
        qiniu_obj = qiniu_upload_img.QiNiu(img_name)
        img_url = qiniu_obj.upload_data(img_info.body)

        if img_url:
            user.avatar = 'http://' + img_url  # 更新用户头像
            user.update()
            self.write_success(data=img_url)
        else:
            self.write_fail(message=u'上传图片失败')