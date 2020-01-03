#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : base_fetch_agent.py
# @Author: Cedar
# @Date  : 2019/12/21
# @Desc  :


import configparser
import os


# 用os模块来读取
curpath = os.path.dirname(os.path.realpath(__file__))
# pardir = os.path.pardir
cfgpath = os.path.join(curpath, "config_param.ini")  # 读取到本机的配置文件
# 调用读取配置模块中的类
conf = configparser.RawConfigParser()
conf.read(cfgpath, encoding="utf-8")


class BaseFetchAgent:
    """
    基类，规定输入输出，对外接口
    调用get_fetch_result可根据fetch_type返回相应结果
    """

    def __init__(self, request_params):
        # config参数
        self.config = conf
        # 默认值
        self.agent_type = ''
        self.fetch_type = ''
        # self.target_id = ''
        self.target_express = ''
        self.target_list = ''        # 逗号隔开
        self.page_count = 0
        self.page_url = ''
        # 传入request_params
        # 传入的参数必须是self.__dict__规定的keys
        for param in request_params:
            if param in self.__dict__.keys():
                self.__dict__[param] = request_params[param]

    def get_fetch_result(self):
        return None

