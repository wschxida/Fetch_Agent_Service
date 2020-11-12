#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : match_account_agent.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import random
from service_app.model.base.base_fetch_agent import BaseFetchAgent
import os
import json
import html


class MatchAccountAgent(BaseFetchAgent):
    """
    Hunt down social media accounts by username across social networks
    https://github.com/sherlock-project/sherlock
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
            self.proxies = "http://" + config_proxylist[index]

        print('----------match_account-----------')
        print(self.__dict__)
        print('==========match_account===========')

    def get_fetch_result(self):
        curpath = os.path.dirname(os.path.realpath(__file__))
        account = self.target_express
        proxy = self.proxies
        output = f'{curpath}/result_dir/{account}.txt'
        cmd = f'''python3 {curpath}/sherlock_master/sherlock {account} -o {output}'''
        if proxy:
            cmd = cmd + f' -p {proxy}'
        print(cmd)
        try:
            os.system(cmd)
            status = '1'
            error = ''
        except Exception as e:
            status = '0'
            error = str(e)

        with open(output, mode='r', encoding='utf-8') as f:
            match_result = f.read()
            data = match_result.split('\n')
            data = data[0:-2]

        result = {"status": status, "error": error, "agent_type": "match_account", "data": data}
        json_result = json.dumps(result, ensure_ascii=False)
        # 再进行html编码，这样最终flask输出才是合法的json
        html_result = html.escape(json_result)
        # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
        if self.html_code == '1':
            return html_result
        else:
            return json_result


if __name__ == '__main__':
    params = {
        'target_express': 'bbc',
    }
    vv = MatchAccountAgent(params)
    result = vv.get_fetch_result()
    print(result)

