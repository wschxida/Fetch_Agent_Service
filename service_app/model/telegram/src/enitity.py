#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/1/27
# @Desc  :


import json
import parsedatetime
import datetime
import time


def get_timestamp(time_str):
    p = parsedatetime.Calendar()
    time_struct, parse_status = p.parse(time_str)
    datetime_result = datetime.datetime(*time_struct[:6])
    t = datetime_result.timetuple()
    result = time.mktime(t)
    return result


class GroupEnitity(object):
    def __init__(self):
        super().__init__()
        self.group_id = ""
        self.group_account = ""
        self.group_name = ""
        self.group_type = ""
        self.group_description = ""
        self.group_url = ""

        self.group_avatar_url = ""
        self.group_avatar_base64 = ""
        self.group_avatar_store_directory_root = ""
        self.group_avatar_local_filename = ""

        self.group_member_count = 0
        self.group_create_time = None

        self.members = []

    def initWithGroup(self, group):
        self.group_id = group.id
        # 提取username
        if group.username is not None:
            self.group_account = group.username
            url = "https://t.me/" + group.username
            self.group_url = url
        if group.title is not None:
            self.group_name = group.title
        self.group_type = "telegram"
        self.group_create_time = group.date.strftime('%Y-%m-%d %H:%M:%S')

    def set_Avatar(self, path, filename):
        self.group_avatar_store_directory_root = path
        temp = filename.split('\\')
        self.group_avatar_local_filename = temp[-1]
        self.group_avatar_url = filename

    def set_Member_Account(self,account):
        self.group_member_count = account

    def add_Member(self,mem,flag=False):
        if flag :
            self.members = []
        self.members.append(mem)


class MessageEnitity(json.JSONEncoder):
    def __init__(self):
        super().__init__()
        self.id = ""
        self.author_account = ""
        self.author_name = ""
        self.media_type_code = False
        self.article_title = "M"

        self.article_url = ""
        self.domain_code = ""
        self.article_pubtime_str = ""
        self.article_pubtime = ""


class MemberEnitity(object):
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
        if picurl is not None:
            self.member_avatar_define = self.member_account+".jpg"


class ChannelEnitity(object):
    def __init__(self):
        super().__init__()
        self.channel_id = ""
        self.channel_account = ""
        self.channel_name = ""
        self.channel_type = ""
        self.channel_description = ""
        self.channel_url = ""

        self.channel_avatar_url = ""
        self.channel_avatar_base64 = ""
        self.channel_avatar_store_directory_root = ""
        self.channel_avatar_local_filename = ""

        self.channel_member_count = 0
        self.channel_create_time = None

        self.members = []

    def initWithChannel(self, channel):
        self.channel_id = channel.id
        # 提取username
        if channel.username is not None:
            self.channel_account = channel.username
            url = "https://t.me/" + channel.username
            self.channel_url = url
        if channel.title is not None:
            self.channel_name = channel.title
        self.channel_type = "telegram"
        self.channel_create_time = channel.date.strftime('%Y-%m-%d %H:%M:%S')
        self.channel_member_count = channel.participants_count

    def set_Avatar(self, path, filename):
        self.channel_avatar_store_directory_root = path
        self.channel_avatar_local_filename = filename.split('/')[-1]
        self.channel_avatar_url = filename

    def add_Member(self, mem, flag=False):
        if flag:
            self.members = []
        self.members.append(mem)
