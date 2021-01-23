#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : instagram_agent.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


from lxml import etree
import html
import json
import random
import requests
from service_app.model.base.base_fetch_agent import BaseFetchAgent


class InstagramAgent(BaseFetchAgent):
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

        print('----------instagram-----------')
        print(self.__dict__)
        print('==========instagram===========')

    def get_fetch_result(self):
        if self.fetch_type == 'get_profile':
            return self.get_profile()
        else:
            return ''

    def get_profile(self, html_code='0'):
        target_profile = []
        try:
            url = f'http://127.0.0.1:5000/service_app?agent_type=instagram&page_type=get_author_id&target_express={self.target_express}'
            # url = 'http://localhost:63342/Fetch_Agent_Service/instagram/profile.html?_ijt=5gh55a61du725grugr7jfo9pro'
            response = requests.get(url)
            response.encoding = 'utf-8'
            root = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
            source = root.xpath('//pre/text()')[0]
            user = json.loads(source)['graphql']['user']
            author_profile_dict = {
                "author_id": user.get("id", ""),
                "author_account": user.get("username", ""),
                "author_name": user.get("full_name", ""),
                "author_url": f'https://www.instagram.com/{user.get("username", "")}/',
                "author_img_url": user.get("profile_pic_url", ""),
                "author_message_count": user.get("edge_owner_to_timeline_media", "").get("count", ""),
                "author_following_count": user.get("edge_follow", "").get("count", ""),
                "author_follower_count": user.get("edge_followed_by", "").get("count", ""),
                "author_description": user.get("biography", ""),
            }
            target_profile.append(author_profile_dict)
            status = '1'
            error = None

        except Exception as e:
            print(e)
            status = '0'
            error = str(e)

        result = {"status": status, "error": error, "agent_type": "instagram", "fetch_type": "get_profile",
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
        'target_express': 'bill',
    }
    vv = InstagramAgent(param)
    data = vv.get_profile()
    print(data)

