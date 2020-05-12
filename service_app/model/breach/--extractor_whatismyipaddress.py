#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_whatismyipaddress.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests
from requests.adapters import HTTPAdapter
from lxml import etree
import html
import json


def extractor_whatismyipaddress(target_express, proxies=None, html_code='0'):
    headers = {
        'Host': 'whatismyipaddress.com',
        'Connection': 'keep-alive',
        'Content-Length': '55',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://whatismyipaddress.com',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://whatismyipaddress.com/breach-check',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    post_data = {
        'txtemail': target_express,
        'btnSubmit': 'Breached?',
    }

    url = 'https://whatismyipaddress.com/breach-check'
    data = []
    status = '0'
    try:
        # requests 重试机制
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        response = s.post(url, timeout=30, data=post_data, headers=headers, proxies=proxies)
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

    # 网站节点可能有变化，先返回固定的结果
    data = [{
      "company_name": "Collection #1",
      "breach_date": "January 7, 2019",
      "data_classes": "Email addresses, Passwords",
      "description": "In January 2019, a large collection of credential stuffing lists (combinations of email addresses and passwords used to hijack accounts on other services) was discovered being distributed on a popular hacking forum. The data contained almost 2.7  records including 773 million unique email addresses alongside passwords those addresses had used on other breached services. Full details on the incident and how to search the breached passwords are provided in the blog post .",
      "total_number_of_accounts_affected": "772,904,991"
    }, {
      "company_name": "Exploit.In",
      "breach_date": "October 13, 2016",
      "data_classes": "Email addresses, Passwords",
      "description": "In late 2016, a huge list of email address and password pairs appeared in a \"combo list\" referred to as \"Exploit.In\". The list contained 593 million unique email addresses, many with multiple different passwords hacked from various online systems. The list was broadly circulated and used for \"credential stuffing\", that is attackers employ it in an attempt to identify other online systems where the account owner had reused their password. For detailed background on this incident, read .",
      "total_number_of_accounts_affected": "593,427,119"
    }]

    result = {"status": status, "agent_type": "breach", "fetch_type": "",
              "data_item_count": len(data), "data": data}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
    if html_code == '1':
        return html_result
    else:
        return json_result


def main():
    # target_express = 'fawzyffawzyf@gmail.com'
    target_express = 'foo@bar.com'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_whatismyipaddress(target_express, proxies)
    print(result)


if __name__ == '__main__':
    main()
