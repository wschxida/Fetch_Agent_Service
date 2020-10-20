#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : youtube_dl_agent.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import random
from service_app.model.base.base_fetch_agent import BaseFetchAgent
from service_app.model.youtube_dl.extractor_youtube_dl import extractor_youtube_dl


class YoutubeDlAgent(BaseFetchAgent):
    """
    youtube_dl类
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

        print('----------youtube_dl-----------')
        print(self.__dict__)
        print('==========youtube_dl===========')

    def get_fetch_result(self):

        result = extractor_youtube_dl(self.target_express, self.proxies, self.html_code)
        return result


if __name__ == '__main__':
    target_express = 'https://twitter.com/i/videos/tweet/1317908612962988033'
    ydl = YoutubeDlAgent(target_express)
    aa = ydl.get_fetch_result()
    print(aa)
