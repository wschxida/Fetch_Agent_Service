#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_common_follower.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests


def extractor_get_common_follower(target_list, proxies=None):
    headers = {
        'Host': 'tweepdiff.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    target_account_list = target_list.split(",")
    url_account = ''
    for account in target_account_list:
        url_account = url_account + account + '.followers/'
    url = 'https://tweepdiff.com/' + url_account + '?n=1000'
    response = requests.get(url, headers=headers, timeout=30, proxies=proxies)
    response.encoding = "utf-8"
    text = response.text
    return text


def main():
    target_list = 'BillGates,Oprah'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_get_common_follower(target_list, proxies)
    print(result)


if __name__ == '__main__':
    main()
