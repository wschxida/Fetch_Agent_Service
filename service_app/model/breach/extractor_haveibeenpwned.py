#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_haveibeenpwned.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests
from requests.adapters import HTTPAdapter
import html
import json


def extractor_haveibeenpwned(target_express, proxies=None, html_code='0'):

    API_KEY = '90ff5f0a72ef4e76a7d66f9fe94e8840'
    headers = {'hibp-api-key': API_KEY}
    url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{target_express}?truncateResponse=false'
    data = []
    status = '0'
    try:
        # requests 重试机制
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        response = s.get(url, timeout=30, headers=headers)
        response.encoding = "utf-8"
        if response.content:
            status = '1'

        items = json.loads(response.content)
        # print(items)
        for item in items:

            company_name = item["Name"]
            breach_date = item["BreachDate"]
            data_classes = item["DataClasses"]
            data_classes = ', '.join(data_classes)

            description = item["Description"]
            total_number_of_accounts_affected = item["PwnCount"]

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
    result = extractor_haveibeenpwned(target_express, proxies)
    print(result)


if __name__ == '__main__':
    main()
