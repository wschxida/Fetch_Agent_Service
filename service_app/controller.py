#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : controller.py
# @Author: Cedar
# @Date  : 2019/12/21
# @Desc  : Agent管理器，根据website_name,分发任务给到不同Agent对象去执行


from service_app.model.facebook_agent import FacebookAgent
from service_app.model.instagram_agent import InstagramAgent


class PageAgentManager:
    """
    Agent服务管理器，根据web请求的类型，来分发模块处理
    """

    def __init__(self, params):
        self.request_params = params

    def get_page_content_by_agent(self):

        cur_page_agent = None

        if self.request_params['website_name'] == 'instagram':
            cur_page_agent = InstagramAgent(self.request_params)
        if self.request_params['website_name'] == 'facebook':
            cur_page_agent = FacebookAgent(self.request_params)

        response = cur_page_agent.get_page_content_by_request()

        return response


