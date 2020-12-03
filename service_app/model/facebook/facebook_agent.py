#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : facebook_agent.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import random
import requests
from service_app.model.base.base_fetch_agent import BaseFetchAgent


class FacebookAgent(BaseFetchAgent):
    """
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

        print('----------facebook-----------')
        print(self.__dict__)
        print('==========facebook===========')

    def get_fetch_result(self):
        if self.fetch_type == 'get_facebook_id':
            return self.find_facebook_id()
        else:
            return ''

    def find_facebook_id(self):
        headers = {
            'Host': 'findmyfbid.in',
            'Connection': 'keep-alive',
            'Content-Length': '104',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://findmyfbid.in',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.52',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://findmyfbid.in/finding-facebook-id/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
        data = {
            'fburl': 'https://www.facebook.com/{}'.format(self.target_express),
        }
        url = 'https://findmyfbid.in/'
        response = requests.post(url, proxies=self.proxies, headers=headers, data=data, allow_redirects=False)
        response_headers = response.headers
        print(response_headers)
        location = response_headers['Location']
        fb_id = location.split('/success/')[1].replace('/', '')
        return fb_id


if __name__ == '__main__':
    params = {
        'target_express': 'bnbarry34',
    }
    vv = FacebookAgent(params)
    result = vv.find_facebook_id()
    print(result)

