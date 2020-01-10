#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_deleted_tweet.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests
from lxml import etree
import html
import json
import re


def extractor_get_deleted_tweet(target_account, proxies=None):
    headers = {
        'Host': 'politwoops.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    url = 'https://politwoops.com/p/unknown/' + target_account
    # url = 'https://politwoops.com/p/unknown/RCoteNPD'
    author_list = []
    status = '0'
    try:
        response = requests.get(url, headers=headers, timeout=30, proxies=proxies)
        response.encoding = "utf-8"
        # 请求成功时就把status置为1,不管后面是否有数据
        if response.content:
            status = '1'
        root = etree.HTML(response.content, parser=etree.HTMLParser(encoding='utf-8'))
        items = root.xpath('//div[contains(@class,"tweet-container")]')
        for item in items:
            # 不要写item.xpath('.//a[@class="person_link"]/text()')[0]，有可能导致list out of index
            # author_id = "".join(item.xpath('.//div/@data-user-id'))
            author_account = target_account
            author_name = "".join(item.xpath('.//a[@class="user_name"]/text()'))
            author_url = "https://twitter.com/" + author_account
            author_img_url = "".join(item.xpath('.//img[@class="img-responsive"]/@src'))
            article_id = "".join(item.xpath('.//div[@class="tweet row"]/@id')).replace('tweet-', '')
            article_url = author_url + "/status/" + article_id
            article_content = "".join(item.xpath('.//div[contains(@class,"tweet-content")]//text()'))

            author_item = {
                # "author_id": author_id,
                "author_account": author_account,
                "author_name": author_name,
                "author_url": author_url,
                "author_img_url": author_img_url,
                "article_url": article_url,
                "article_content": article_content,
            }
            author_list.append(author_item)

    except Exception as e:
        status = str(e)
        print(e)

    result = {"status": status, "agent_type": "twitter", "fetch_type": "get_deleted_tweet",
              "data": author_list}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    return html_result


def main():
    target_account = 'RCoteNPD'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_get_deleted_tweet(target_account, proxies)
    print(result)


if __name__ == '__main__':
    main()
