#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : breach_agent.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import random
from service_app.model.base.base_fetch_agent import BaseFetchAgent
from service_app.model.breach.extractor_whatismyipaddress import extractor_whatismyipaddress


class BreachAgent(BaseFetchAgent):
    """
    breach类
    调用get_fetch_result可根据fetch_type返回相应结果
    """

    def __init__(self, params):
        # 初始化积累参数
        BaseFetchAgent.__init__(self, params)

        # 取出config，自己需要的参数
        self.proxies = None
        config_proxylist = self.config.get("proxy", "proxylist")
        # 转成list
        if config_proxylist:
            config_proxylist = config_proxylist.split("||")
            # proxy根据全局参数里面的设置，随机选取一个
            index = random.randint(0, len(config_proxylist) - 1)
            self.proxies = {
                'http': "http://" + config_proxylist[index],
                'https': "http://" + config_proxylist[index]
            }

        print('----------Breach-----------')
        print(self.__dict__)
        print('==========Breach===========')

    def get_fetch_result(self):
        result_whatismyipaddress = extractor_whatismyipaddress(self.target_express, self.proxies, self.html_code)
        if result_whatismyipaddress is not None:
            return result_whatismyipaddress
        else:
            return None
