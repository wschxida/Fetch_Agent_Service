#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_tweet_of_url.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests
from requests.adapters import HTTPAdapter
import html
import json


def extractor_get_tweet_of_url(query='{}', proxies=None, html_code='0'):
    status = '1'
    error = None
    data = ''
    try:
        query_dict = json.loads(query)
        url = query_dict['url']
        # return url
        proxy_ip = 'lum-customer-hl_7cc83d7d-zone-twitter:lk092yxnhj4j@zproxy.lum-superproxy.io:22225'
        if not proxies:
            proxies = {'http': f'http://{proxy_ip}', 'https': f'http://{proxy_ip}'}

        # requests 重试机制
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))

        if 'mobile.twitter' not in url:
            url = 'https://mobile.twitter.com/' + url
        response = s.get(url, proxies=proxies, timeout=10)
        response.encoding = "utf-8"
        data = response.text
        # 输出结果为json
        result = {"status": status, "error": error, "agent_type": "twitter", "fetch_type": "get_tweet_of_url",
                  "target_profile": "",
                  "data_item_count": "", "data": data}
        json_result = json.dumps(result, ensure_ascii=False)
        # 再进行html编码，这样最终flask输出才是合法的json
        html_result = html.escape(json_result)
        # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
        if html_code == '1':
            return html_result
        else:
            return json_result

    except Exception as e:
        result = {"status": 0, "error": str(e), "agent_type": "twitter", "fetch_type": "get_tweet_of_url",
                  "target_profile": "",
                  "data_item_count": "", "data": ""}
        json_result = json.dumps(result, ensure_ascii=False)
        return json_result


def main():

    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    query = '''
    {"url": "BBC/status/1306292012916695040"}
    '''

    result = extractor_get_tweet_of_url(query, proxies)
    print(result)


if __name__ == '__main__':
    main()
