#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_mutual_follower.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests
from requests.adapters import HTTPAdapter
from lxml import etree
import html
import json
import re
from service_app.model.twitter.extractor.common_function.extractor_get_author_profile import extractor_get_author_profile


def extractor_get_mutual_follower(target_list, proxies=None, page_count=1, html_code='0'):

    target_account_list = target_list.split(",")
    target_profile = []
    for target_account in target_account_list:
        target_account_profile = extractor_get_author_profile(target_account, proxies)
        target_profile.append(target_account_profile)

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

    # 设置获取条数
    n = 20
    if int(page_count) > 0:
        n = 20 * int(page_count)
    url = 'https://tweepdiff.com/' + url_account + f'?n={n}'
    # url = 'https://tweepdiff.com/BillGates.followers/BillClinton.followers/?n=100'
    author_list = []
    status = '0'
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
        status = str(e)
        print(e)

    result = {"status": status, "agent_type": "twitter", "fetch_type": "get_mutual_follower", "target_profile": target_profile,
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
    target_list = 'BillGates,BillClinton'
    proxies = {
        'http': 'http://127.0.0.1:4411',
        'https': 'http://127.0.0.1:4411'
    }
    result = extractor_get_mutual_follower(target_list, proxies)
    print(result)


if __name__ == '__main__':
    main()
