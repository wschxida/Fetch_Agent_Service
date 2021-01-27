#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_deleted_tweet.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests
from requests.adapters import HTTPAdapter
from lxml import etree
import html
import json
import parsedatetime
import datetime
import time
from service_app.model.twitter.extractor.lib.get_author_profile import get_author_profile
from service_app.model.twitter.extractor.lib.clean_html_attr import clean_html_attr
from service_app.model.twitter.extractor.extractor_get_tweet_of_suspended_author import extractor_get_tweet_of_suspended_author


def extractor_get_deleted_tweet(target_account, proxies=None, page_count=1, html_code='0'):

    target_profile = []
    target_account_profile = get_author_profile(target_account, proxies)
    if target_account_profile:
        target_profile.append(target_account_profile)

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
    # url = 'https://projects.propublica.org/politwoops/user/realDonaldTrump'
    author_list = []
    status = '0'
    error = None
    try:
        response_list = []
        for i in range(int(page_count)):
            _url = url + f'?page={i+1}'
            # requests 重试机制
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            response = s.get(_url, headers=headers, timeout=30, proxies=proxies)
            response.encoding = "utf-8"
            response_list.append(response.content)

        for response_item in response_list:

            # 只要有成功返回的item，就认为是请求成功
            if len(response_item) > 0:
                status = '1'

            root = etree.HTML(response_item, parser=etree.HTMLParser(encoding='utf-8'))
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
                _article_pubtime = "".join(item.xpath('.//div[contains(@class,"byline")]/a[@data-content]/@data-content'))
                article_content = "".join(item.xpath('.//div[contains(@class,"tweet-content")]//text()'))
                article_content = clean_html_attr(article_content)  # html清洗

                # 时间转换为时间戳
                p = parsedatetime.Calendar()
                time_struct, parse_status = p.parse(_article_pubtime)
                datetime_result = datetime.datetime(*time_struct[:6])
                t = datetime_result.timetuple()
                article_pubtime = int(time.mktime(t))

                author_item = {
                    # "author_id": author_id,
                    "author_account": author_account,
                    "author_name": author_name,
                    "author_url": author_url,
                    "author_img_url": author_img_url,
                    "article_url": article_url,
                    "article_pubtime": article_pubtime,
                    "article_content": article_content,
                }
                author_list.append(author_item)

    except Exception as e:
        status = '0'
        error = str(e)
        print(e)

    # 如果抓不到数据，从wayback搜索
    if len(author_list) == 0:
        _result = extractor_get_tweet_of_suspended_author(target_account, proxies)
        _json = json.loads(_result)
        target_profile = _json['target_profile']
        author_list = _json['data']

    result = {"status": status, "error": error, "agent_type": "twitter", "fetch_type": "get_deleted_tweet", "target_profile": target_profile,
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
    # target_account = 'RCoteNPD'
    target_account = 'realDonaldTrump'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_get_deleted_tweet(target_account, proxies)
    print(result)
    #     https://polititweet.org/figure?account=25073877


if __name__ == '__main__':
    main()
