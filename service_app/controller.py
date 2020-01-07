#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : controller.py
# @Author: Cedar
# @Date  : 2019/12/21
# @Desc  : Agent管理器，根据agent_type,分发任务给到不同Agent对象去执行


from service_app.model.twitter.twitter_agent import TwitterAgent
from service_app.model.breach.breach_agent import BreachAgent


class FetchAgentManager:
    """
    Agent服务管理器，根据web请求的类型，来分发模块处理
    """

    def __init__(self, params):
        self.request_params = params

    def get_fetch_result_by_agent(self):

        cur_fetch_agent = None

        if self.request_params['agent_type'] == 'twitter':
            cur_fetch_agent = TwitterAgent(self.request_params)
        if self.request_params['agent_type'] == 'breach':
            cur_fetch_agent = BreachAgent(self.request_params)

        response = cur_fetch_agent.get_fetch_result()

        return response


