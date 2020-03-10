#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_author_reply_to_the_target.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests
from requests.adapters import HTTPAdapter
from lxml import etree
import html
import json


def extractor_get_author_reply_to_the_target(target_account, proxies=None, page_count=1):
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

    q = '(to%3A' + target_account + ')%20-filter%3Alinks%20filter%3Areplies'
    url = 'https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=' + q + '&src=typd&include_available_features=1&include_entities=1&reset_error_state=false&max_position='

    author_list = []
    status = '0'
    try:
        prefix = url
        _url = prefix
        has_more_items = True
        response_list = []
        page_request = 1
        while has_more_items is True:
            # requests 重试机制
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            response = s.get(_url, headers=headers, timeout=30, proxies=proxies)
            if response is not None:
                try:
                    json_data = json.loads(response.content, strict=False)
                    has_more_items = json_data.get("has_more_items")
                    min_position = json_data.get("min_position")
                    _url = prefix + min_position
                except json.decoder.JSONDecodeError:
                    pass
            response.encoding = "utf-8"
            response_list.append(response.content)

            page_request += 1
            if page_request > int(page_count):
                break

        for response_item in response_list:
            response_json = json.loads(response_item)
            items_html = response_json["items_html"]
            # 请求成功时就把status置为1,不管后面是否有数据
            if items_html:
                status = '1'
            root = etree.HTML(items_html, parser=etree.HTMLParser(encoding='utf-8'))
            items = root.xpath('//li[@data-item-type="tweet"]')
            for item in items:
                # 不要写item.xpath('.//a[@class="person_link"]/text()')[0]，有可能导致list out of index
                author_id = "".join(item.xpath('.//div/@data-user-id'))
                author_account = "".join(item.xpath('.//div/@data-screen-name'))
                author_name = "".join(item.xpath('.//div/@data-name'))
                author_url = "https://twitter.com/" + author_account
                author_img_url = "".join(item.xpath('.//img[@class="avatar js-action-profile-avatar"]/@src'))
                article_url = "https://twitter.com" + "".join(item.xpath('.//div/@data-permalink-path'))
                article_content = item.find('.//div[@class="js-tweet-text-container"]')
                article_content = etree.tostring(article_content)  # 转为bytes
                article_content = str(article_content, encoding="utf-8")  # 转为字符串

                author_item = {
                    "author_id": author_id,
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

    # 输出结果为json
    result = {"status": status, "agent_type": "twitter", "fetch_type": "get_author_reply_to_the_target",
              "data_item_count": len(author_list), "data": author_list}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    return html_result


def main():
    target_account = 'BillGates'
    proxies = {
        'http': 'http://127.0.0.1:4411',
        'https': 'http://127.0.0.1:4411'
    }
    result = extractor_get_author_reply_to_the_target(target_account, proxies)
    print(result)


if __name__ == '__main__':
    main()
