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

    try:
        query_dict = json.loads(query)
        url = query_dict['url']

    except Exception as e:
        url = ''
        status = '0'
        error = str(e)
        print(e)

    proxy_ip = 'lum-customer-hl_7cc83d7d-zone-twitter:lk092yxnhj4j@zproxy.lum-superproxy.io:22225'
    if not proxies:
        proxies = {'http': f'http://{proxy_ip}', 'https': f'http://{proxy_ip}'}
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "referer": "https://twitter.com/search",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "cookie": "rweb_optin=side_no_out"
    }
    # requests 重试机制
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    try:
        if ("mobile" or "gettwitterid") in url:
            print(1)
            response = s.get(url, timeout=10)
        else:
            print(2)
            response = s.get(url, proxies=proxies, headers=headers, timeout=10)
        response.encoding = "utf-8"
        data = response.text
        status = '1'
        error = None

    except Exception as e:
        print(str(e))
        data = ''
        status = '0'
        error = e

    # 输出结果为json
    result = {"status": status, "error": error, "agent_type": "twitter", "fetch_type": "get_tweet_of_url", "target_profile": "",
              "data_item_count": "", "data": data}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
    if html_code == '1':
        return html_result
    else:
        return json_result


def main():

    proxies = {
        'http': 'http://127.0.0.1:4411',
        'https': 'http://127.0.0.1:4411'
    }
    query = '''
    {"url": "https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=(from%3AVOAChinese)&src=typd&include_available_features=1&include_entities=1&reset_error_state=false&max_position="}
    '''

    result = extractor_get_tweet_of_url(query, proxies)
    print(result)


if __name__ == '__main__':
    main()
