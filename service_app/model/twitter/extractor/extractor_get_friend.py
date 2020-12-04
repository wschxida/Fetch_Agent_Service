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
from requests.adapters import HTTPAdapter
from lxml import etree
import html
import json
import re
from service_app.model.twitter.extractor.lib.get_author_profile import get_author_profile
from service_app.model.twitter.extractor.lib.get_common_friend_by_tweepdiff import get_common_friend_by_tweepdiff


def extractor_get_friend(target_account, user_data_dir_list, proxies=None, html_code='0'):

    target_profile = []
    target_account_profile = get_author_profile(target_account, proxies)
    if target_account_profile:
        target_profile.append(target_account_profile)

    url = 'https://tweepdiff.com/' + target_account + '/' + target_account + f'.followers?n=1000'
    # url = 'https://tweepdiff.com/KimberBollacker/KimberBollacker.followers?n=1000'
    author_list = []
    error = None
    try:
        author_list = [] + get_common_friend_by_tweepdiff(url, proxies)
        status = '1'

    except Exception as e:
        status = '0'
        error = str(e)
        print(e)

    result = {"status": status, "error": error, "agent_type": "twitter", "fetch_type": "get_friend", "target_profile": target_profile,
              "data_item_count": len(author_list), "data": author_list}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
    if html_code == '1':
        return html_result
    else:
        return json_result


def main():
    target_account = 'carolineparra4'
    user_data_dir_list = ['E:\\selenium\\AutomationProfile1']
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_get_friend(target_account, user_data_dir_list, proxies)
    print(result)


if __name__ == '__main__':
    main()
