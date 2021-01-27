#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


from lxml import etree
import html
import json
import random
import requests
from service_app.model.base.base_fetch_agent import BaseFetchAgent


def get_middle_str(content, start_str, end_str):
    """通用函数，获取前后两个字符串中间的内容"""
    try:
        start_index = content.index(start_str)
        if start_index >= 0:
            start_index += len(start_str)
        content = content[start_index:]
        end_index = content.index(end_str)
        return content[:end_index]
    except Exception as e:
        return None


class VkAgent(BaseFetchAgent):
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

        print('----------VK-----------')
        print(self.__dict__)
        print('==========VK===========')

    def get_fetch_result(self):
        if self.fetch_type == 'get_profile':
            return self.get_profile()
        else:
            return ''

    def get_profile(self, html_code='0'):
        target_profile = []
        try:
            url = f'https://vk.com/{self.target_express}'
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
                "cache-control": "max-age=0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "cross-site",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
            }
            response = requests.get(url, proxies=self.proxies, headers=headers)
            response.encoding = 'utf-8'
            # root = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
            author_profile_dict = {
                "author_id": get_middle_str(response.text, 'https://vk.com/id', '"'),
                "author_account": self.target_express,
                "author_name": get_middle_str(response.text, '<meta property="og:title" content="', '"'),
                "author_url": url,
            }
            target_profile.append(author_profile_dict)
            status = '1'
            error = None

        except Exception as e:
            print(e)
            status = '0'
            error = str(e)

        result = {"status": status, "error": error, "agent_type": "VK", "fetch_type": "get_profile",
                  "target_profile": target_profile, "data_item_count": 1, "data": ''}
        json_result = json.dumps(result, ensure_ascii=False)
        # 再进行html编码，这样最终flask输出才是合法的json
        html_result = html.escape(json_result)
        # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
        if html_code == '1':
            return html_result
        else:
            return json_result


if __name__ == '__main__':
    param = {
        'target_express': 'news__ykt',
    }
    vv = VkAgent(param)
    data = vv.get_profile()
    print(data)

