#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : base.py
# @Author: Cedar
# @Date  : 2019/12/21
# @Desc  :


class BasePageAgent:
    """
    基类，规定输入输出，对外接口
    调用get_page_content_by_request可根据page_type返回相应结果
    """

    def __init__(self, request_params):
        # 默认值
        self.website_name = None
        self.page_type = None
        self.target_id = None
        self.target_account = None
        self.page_count = 0
        self.page_url = None
        # 传入request_params
        # 传入的参数必须是self.__dict__规定的keys
        for param in request_params:
            if param in self.__dict__.keys():
                self.__dict__[param] = request_params[param]

    def get_page_content_by_request(self):
        return None

