#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_friend.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :
# Get the common users both in follower and following list.
# They are the friends of the target.
# They follow each other.
# They have tight relationship.


import requests


def extractor_get_friend(target_account, proxies=None):
    headers = {
        'Host': 'tweepdiff.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    url = 'https://tweepdiff.com/' + target_account + '/' + target_account + '.followers?n=1000'
    # url = 'https://tweepdiff.com/KimberBollacker/KimberBollacker.followers?n=1000'
    response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
    response.encoding = "utf-8"
    text = response.text
    return text


def main():
    target_account = 'KimberBollacker'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_get_friend(target_account, proxies)
    print(result)


if __name__ == '__main__':
    main()
