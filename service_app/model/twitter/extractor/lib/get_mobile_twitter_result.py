#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : get_mobile_twitter_result.py
# @Author: Cedar
# @Date  : 2020/10/14
# @Desc  :


from requests.adapters import HTTPAdapter
import json
from lxml import etree
import requests
import datetime


def get_html(url, proxies):
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        response = s.get(url, timeout=30, proxies=proxies)
        return response.text

    except Exception as e:
        print(str(e))


def parse_html(response_text):
    """
    解析获取到的message_html源码，提取必须字段，索引至ES
    :return:
    """
    try:
        res_byte = bytes(response_text, encoding="utf-8")
        data_list = []
        result_html = etree.HTML(res_byte)
        items = result_html.xpath('//table[contains(@class,"tweet")]')
        for i, article in enumerate(items):
            data = {}
            data['author_id'] = ''
            data['author_name'] = "".join(article.xpath('.//strong[@class="fullname"]/text()'))
            data['author_img_url'] = "".join(article.xpath('.//td[@class="avatar"]/a/img/@src'))
            article_url = "".join(article.xpath('.//td[@class="timestamp"]/a[1]/@href')).split('?')[0]
            data['article_url'] = f"https://twitter.com{article_url}"
            data['author_account'] = data['article_url'].split('twitter.com/')[1].split('/status/')[0]
            data['author_url'] = 'https://twitter.com/' + data['author_account']
            publish_time_str = "".join(article.xpath('.//td[@class="timestamp"]/a[1]/text()'))
            data['article_pubtime'] = date_format(publish_time_str)
            data['article_content'] = str(etree.tostring(article.xpath('.//td[@class="tweet-content"]')[0], encoding='utf-8'), encoding="utf-8")
            # article_content = clean_html_attr(article_content)  # html清洗

            data_list.append(data)
        next_cursor = result_html.xpath("//div[@class='w-button-more']/a[1]/@href")
        error_page = result_html.xpath("//div[@class='system']//text()")
        return [data_list, next_cursor, error_page]

    except:
        return None


def date_format(time_str):
    """
    mobile接口的列表数据没有时间戳，只有时间字符串。改函数作用为修改时间字符串为标准时间格式
    :param time_str: 列表上的时间字符串，格式为2s,5        time_str = int(time_str.replace("s", ''))
m,6h,March 24....
    :return:
    """
    current_time = datetime.datetime.now()
    if time_str.endswith("s"):
        time_str = int(time_str.replace("s", ''))
        time_difference = datetime.timedelta(seconds=time_str)
        publish_time_str = current_time - time_difference
        format_time = publish_time_str.strftime('%Y-%m-%d %H:%M:%S')
    elif time_str.endswith("m"):
        time_str = int(time_str.replace("m", ''))
        time_difference = datetime.timedelta(minutes=time_str)
        publish_time_str = current_time - time_difference
        format_time = publish_time_str.strftime('%Y-%m-%d %H:%M:%S')
    elif time_str.endswith("h"):
        time_str = int(time_str.replace("h", ''))
        time_difference = datetime.timedelta(hours=time_str)
        publish_time_str = current_time - time_difference
        format_time = publish_time_str.strftime('%Y-%m-%d %H:%M:%S')
    else:
        time_list = time_str.split(' ')
        if len(time_list) == 3:
            year = "20" + time_list[-1]
            month = time_list[1]
            date = time_list[0]
            time_str = f"{year}-{month}-{date}"
            format_time = time_str
        else:
            format_time = datetime.datetime.strptime('2020 ' + time_str, '%Y %b %d')
            time_difference = str(current_time-format_time)
            if '-' in time_difference:
                format_time = datetime.datetime.strptime('2019 ' + time_str, '%Y %b %d')
            format_time = str(format_time)
    return format_time


def get_tweet(url, page_count=1, proxies=None):
    result = []
    url_prefix = url
    for i in range(int(page_count)):
        try:
            # print(url)
            response_text = get_html(url, proxies)
            page_content = parse_html(response_text)
            data_list = page_content[0]
            next_cursor = page_content[1]
            error_page = page_content[2]
            result = result + data_list

            if len(next_cursor) > 0:
                next_cursor = next_cursor[0].split('=')[-1]
                url = f"{url_prefix}&next_cursor={next_cursor}"
            else:
                break
        except Exception as e:
            print(str(e))
            return str(e)

    return result


def main():
    url = 'https://mobile.twitter.com/search?q=%28@BBC%29+-filter%3Areplies+-filter%3A%28from%3A-BBC%29+&s=typd&x=26&y=23&f=live'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = get_tweet(url, 2, proxies)
    json_result = json.dumps(result)
    print(json_result)
    print(len(result))


if __name__ == '__main__':
    main()
