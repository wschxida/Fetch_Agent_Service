#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : get_common_friend_by_tweepdiff.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests
from requests.adapters import HTTPAdapter
from lxml import etree
import html
import json
import re


def get_common_friend_by_tweepdiff(url, proxies=None):

    headers = {
        'Host': 'tweepdiff.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    author_list = []
    try:
        # requests 重试机制
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        response = s.get(url, headers=headers, timeout=30, proxies=proxies)
        response.encoding = "utf-8"
        # 请求成功时就把status置为1,不管后面是否有数据
        if response.content:
            status = '1'
        root = etree.HTML(response.content, parser=etree.HTMLParser(encoding='utf-8'))
        items = root.xpath('//div[@class="person"]')
        for item in items:
            # 不要写item.xpath('.//a[@class="person_link"]/text()')[0]，有可能导致list out of index
            # author_id页面上没有
            # author_id = ""
            author_account = "".join(item.xpath('.//a[@class="person_link"]/text()'))
            author_account = "".join(re.findall("[(](.*?)[)]", author_account))  # 取括号里面的字符
            author_name = "".join(item.xpath('.//a[@class="person_link"]/text()'))
            author_name = "".join(re.findall("[\n](.*)[(]", author_name))  # 取\n和(之间的字符
            author_url = "".join(item.xpath('.//h2/a/@href'))
            author_img_url = "".join(item.xpath('.//h2//img/@src'))
            author_description = "".join(item.xpath('.//div[@class="bio"]/span[2]/text()'))
            author_follower_count = "".join(item.xpath('.//div[@class="followers"]/div[@class="count"]/text()'))
            author_following_count = "".join(item.xpath('.//div[@class="friends"]/div[@class="count"]/text()'))
            author_message_count = "".join(item.xpath('.//div[@class="updates"]/div[@class="count"]/text()'))

            author_item = {
                # "author_id": author_id,
                "author_account": author_account,
                "author_name": author_name,
                "author_url": author_url,
                "author_img_url": author_img_url,
                "author_description": author_description,
                "author_follower_count": author_follower_count,
                "author_following_count": author_following_count,
                "author_message_count": author_message_count,
            }
            author_list.append(author_item)

    except Exception as e:
        print(e)

    return author_list


def main():
    url = 'https://tweepdiff.com/JoeForIA.followers/joebidenGA.followers?n=1000'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = get_common_friend_by_tweepdiff(url, proxies)
    print(result)


if __name__ == '__main__':
    main()