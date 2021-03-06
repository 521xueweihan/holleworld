#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/6/12 下午3:14
#   Desc    :   个人页面
import os
import uuid
import logging

from app import UserHandler
from model.models import User, Article
from utilities import qiniu_upload_img


class ProfileHandler(UserHandler):
    @staticmethod
    def del_old_avatar(qiniu_obj, user):
        """
        删除原来的头像
        """
        if user.avatar:
             # 七牛上存的文件名
            avatar_name = user.avatar[7:].split('/')[1]
            # 七牛上删除原来的头像
            del_result = qiniu_obj.del_file(avatar_name)
            if not del_result:
                logging.error('删除用户：{}头像时出错！'.format(user.uid))

    def get(self, uid):
        user = User.find_first('where uid=? and status=0', uid)
        page = int(self.get_argument('page', 1))
        total = Article.count_by('where author_id=? and status=0', user.uid)
        offset, count = self.offset(page)
        articles_list = Article.find_by(
            """where author_id=? and status=0
            order by create_time desc limit ?, ?""", user.uid, offset, count
        )
        has_more = total > offset+count
        for fi_article in articles_list:
            fi_article['warp_id'] = self._warp_id(fi_article['id'])
            fi_article['show_source_url'] = fi_article.source_url.split('://')[1]
            # 原文地址只展示host
            fi_article['show_source_url'] = fi_article['show_source_url'].split('/')[0]
        self.render('profile.html', articles_list=articles_list, uid=uid,
                    has_more=has_more, page=page, count=count, user=user)

    def post(self, uid):
        """
        更新用户信息（暂时只做了上传头像）
        """
        user = User.find_first('where uid=? and status=0', uid)
        if not user:
            self.write_fail(message=u'用户不存在')
        img_info = self.request.files['filearg'][0]
        img_name = img_info['filename']
        extn = os.path.splitext(img_name)[1]
        img_name = str(uuid.uuid4()) + extn
        qiniu_obj = qiniu_upload_img.QiNiu(img_name)
        img_url = qiniu_obj.upload_data(img_info.body)
        if img_url:
            ProfileHandler.del_old_avatar(qiniu_obj, user)
            user.avatar = 'http://' + img_url  # 更新用户头像
            user.update()
            self.write_success(data=img_url)
        else:
            self.write_fail(message=u'上传图片失败')