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
from lxml import etree
import html
import json
import re


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
    author_list = []
    status = '0'
    try:
        response = requests.get(url, headers=headers, timeout=30, proxies=proxies)
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
        status = str(e)
        print(e)

    result = {"status": status, "agent_type": "twitter", "fetch_type": "get_friend",
              "data": author_list}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    return html_result


def main():
    target_account = 'KimberBollacker'
    proxies = {
        'http': 'http://127.0.0.1:4411',
        'https': 'http://127.0.0.1:4411'
    }
    result = extractor_get_friend(target_account, proxies)
    print(result)


if __name__ == '__main__':
    main()
