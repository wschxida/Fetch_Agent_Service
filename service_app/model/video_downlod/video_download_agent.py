#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : video_download_agent.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import random
from model.base.base_fetch_agent import BaseFetchAgent
from model.video_downlod.extractor_youtube_dl import extractor_youtube_dl_def


class VideoDownloadAgent(BaseFetchAgent):
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

        print('----------video_downlod-----------')
        print(self.__dict__)
        print('==========video_downlod===========')

    def get_fetch_result(self):
        result = extractor_youtube_dl_def(self.target_express, self.proxies, self.html_code)
        return result


if __name__ == '__main__':
    params = {
        'target_express': 'https://www.youtube.com/watch?v=qnaZm8JL5rE',
    }
    vv = VideoDownloadAgent(params)
    result = vv.get_fetch_result()
    print(result)

