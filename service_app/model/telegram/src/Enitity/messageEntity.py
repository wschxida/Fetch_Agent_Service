#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_common_follower.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :

import json


class messageEnitity(json.JSONEncoder):
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
