#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_tweet_reply_to_the_target.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests


def extractor_get_tweet_reply_to_the_target(target_account, proxies=None):
    headers = {
        'Host': 'twitter.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    url = 'https://twitter.com/search?q=(to%3A' + target_account + ')%20-filter%3Alinks%20filter%3Areplies&src=typed_query&f=live'
    # url = 'https://twitter.com/search?q=(to%3ACDeeMe2)%20-filter%3Alinks%20filter%3Areplies&src=typed_query&f=live'
    response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
    response.encoding = "utf-8"
    text = response.text
    return text


def main():
    target_account = 'ABC'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_get_tweet_reply_to_the_target(target_account, proxies)
    print(result)


if __name__ == '__main__':
    main()
