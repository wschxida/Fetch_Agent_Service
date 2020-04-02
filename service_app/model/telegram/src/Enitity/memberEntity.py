#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_common_follower.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


class memberEnitity(object):
    def __init__(self):
        self.member_id = ""
        self.member_account = ""
        self.member_name = ""
        self.member_is_administrator = False
        self.member_role = "M"

        self.member_avatar_url = ""
        self.member_avatar_base64 = ""
        self.member_avatar_define = ""
        self.member_description = ""
        self.member_friend_count = None
        self.member_following_count = None
        self.member_follower_count = None
        self.member_mobile = ""
        self.member_email = None
        self.member_profile_url = None,
        self.member_join_time = ""

    def set_id(self, ):
        self.member_id = id

    def set_account(self, account):
        self.member_account = account
        self.member_profile_url = ("https://t.me/" + account).strip()

    def initWithUser(self, user):
        self.member_id = user.id
        # 提取username
        if user.username:
            self.member_account = user.username
            url = ("https://t.me/" + user.username).strip()
            self.member_profile_url = url

        # 提取name
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = ""
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = ""
        name = (first_name + ' ' + last_name).strip()
        self.member_name = name
        self.member_mobile = user.phone

    def set_adminInfo(self, flag):
        self.member_is_administrator = flag
        self.member_role = "A"

    def set_ProfilePic(self, picurl):
        self.member_avatar_url = picurl
        if picurl is not None :
            self.member_avatar_define = self.member_account+".jpg"
