#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :

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
        # print(e)
        return None


def get_author_id(content):
    user_id = get_middle_str(content, 'entity_id:', ',')
    page_id = get_middle_str(content, 'pageID:"', '"')
    if user_id:
        author_id = user_id
    else:
        author_id = page_id
    return author_id


def request_lookup_id(url, proxies):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36",
      }
    data = {
        'fburl': f'{url}',
        'check': 'Lookup',
    }
    url = 'https://lookup-id.com/'
    author_dict = {
        "author_name": "",
        "author_id": "",
    }
    try:
        response = requests.post(url, proxies=proxies, headers=headers, data=data, allow_redirects=True)
        author_name = get_middle_str(response.text, 'name is <em>', '</em>, then we found your numeric ID:')
        author_id = get_middle_str(response.text, '<span id="code">', '</span>')
        author_dict = {
            "author_name": author_name,
            "author_id": author_id,
        }
        return author_dict

    except Exception as e:
        print(e)
        return author_dict


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
        if self.fetch_type == 'get_profile':
            return self.get_profile()
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
        # print(response_headers)
        location = response_headers['Location']
        fb_id = location.split('/success/')[1].replace('/', '')
        return fb_id

    def get_profile(self, html_code='0'):
        target_profile = []
        headers = {
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        basic_url = 'https://m.facebook.com/'

        try:
            # 先判断输入的是account还是url
            if 'http' in self.target_express and 'www.facebook' in self.target_express:
                author_url = self.target_express.replace('www.facebook', 'm.facebook')
                # 如果url以'/'结尾
                if author_url.split('/')[-1] == '':
                    author_account = author_url.split('/')[-2].replace('/', '').replace('profile.php?id=', '')
                else:
                    author_account = author_url.split('/')[-1].replace('/', '').replace('profile.php?id=', '')
            else:
                author_url = basic_url + self.target_express
                author_account = self.target_express

            # 从facebook请求获取id
            response = requests.post(author_url, timeout=30, proxies=self.proxies, headers=headers, allow_redirects=False)
            response.encoding = 'utf-8'
            text = response.text
            author_id = get_author_id(text)

            # 第三方网站获取author_name
            author_dict_from_lookup = request_lookup_id(author_url, self.proxies)
            author_name = author_dict_from_lookup['author_name']
            if len(author_id) == 0:
                author_id = author_dict_from_lookup['author_id']

            author_profile_dict = {
                "author_id": author_id,
                "author_account": author_account,
                "author_name": author_name,
                "author_url": author_url.replace('m.facebook', 'www.facebook'),
            }
            target_profile.append(author_profile_dict)
            status = '1'
            error = None

        except Exception as e:
            print(e)
            status = '0'
            error = str(e)

        result = {"status": status, "error": error, "agent_type": "facebook", "fetch_type": "get_profile",
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
    params = {
        'target_express': 'https://www.facebook.com/groups/cryptofinancialworld/',
    }
    vv = FacebookAgent(params)
    data = vv.get_profile()
    print(data)
    # proxies = {
    #     'http': 'http://127.0.0.1:7777',
    #     'https': 'http://127.0.0.1:7777',
    # }
    # url = 'https://m.facebook.com/bnbarry34'
    # request_lookup_id(url, proxies)

# url = 'https://www.facebook.com/bnbarry34'  # user: 1141684952
# url = 'https://www.facebook.com/joebiden'  # page: 7860876103
# url = 'https://www.facebook.com/profile.php?id=100026514127194'  # user: 100026514127194
# url = 'https://www.facebook.com/groups/432930430071128/'  # group:432930430071128
# url = 'https://www.facebook.com/groups/cryptofinancialworld/'  # group:1231416480213978