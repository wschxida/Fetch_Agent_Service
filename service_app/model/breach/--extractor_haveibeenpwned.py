#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : --extractor_haveibeenpwned.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests
from lxml import etree
import html
import json
import re


# 需要Google reCAPTCHA 验证才能获取cookie，太麻烦
def extractor_haveibeenpwned(target_express, proxies=None):
    headers = {
        'Host': 'haveibeenpwned.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    base_url = 'https://haveibeenpwned.com/'
    url = 'https://haveibeenpwned.com/unifiedsearch/fawzyffawzyf%40gmail.com'
    data = []
    status = '0'
    try:
        session = requests.Session()
        session.proxies = proxies
        session.headers = headers
        req = session.get(base_url)
        req.encoding = "utf-8"
        req.headers
        # session.headers.update({'Cookie': req.cookies})
        response = session.get(url, timeout=30)
        response.encoding = "utf-8"
        if response.content:
            status = '1'
        root = etree.HTML(response.content, parser=etree.HTMLParser(encoding='utf-8'))
        items = root.xpath('//div[@class="breach-wrapper"]')
        for item in items:
            # 不要写item.xpath('.//a[@class="person_link"]/text()')[0]，有可能导致list out of index
            company_name = "".join(item.xpath('.//div[1]/text()'))
            breach_date = "".join(item.xpath('.//div[2]/text()'))
            data_classes = "".join(item.xpath('.//div[3]/text()'))
            description = "".join(item.xpath('.//div[4]/text()'))
            total_number_of_accounts_affected = "".join(item.xpath('.//div[5]/text()'))

            data_item = {
                "company_name": company_name,
                "breach_date": breach_date,
                "data_classes": data_classes,
                "description": description,
                "total_number_of_accounts_affected": total_number_of_accounts_affected,
            }
            data.append(data_item)

    except Exception as e:
        status = str(e)
        print(e)

    result = {"status": status, "agent_type": "breach", "fetch_type": "",
              "data": data}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    return str(req.headers)


def main():
    target_express = 'fawzyffawzyf@gmail.com'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_haveibeenpwned(target_express, proxies)
    print(result)


if __name__ == '__main__':
    main()
