#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : telegram_agent.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


from service_app.model.base.base_fetch_agent import BaseFetchAgent
from service_app.model.telegram.get_member import extractor_get_member
# from service_app.model.telegram.get_message import extractor_get_message


class TelegramAgent(BaseFetchAgent):
    """
    telegram
    调用get_fetch_result可根据fetch_type返回相应结果
    """

    def __init__(self, params):
        # 初始化积累参数
        BaseFetchAgent.__init__(self, params)

    def get_fetch_result(self):
        if self.fetch_type == 'get_member':
            return extractor_get_member(self.target_express)
        # if self.fetch_type == 'get_message':
        #     return extractor_get_message(self.target_express)
