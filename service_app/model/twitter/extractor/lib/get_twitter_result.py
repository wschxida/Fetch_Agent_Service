#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : get_twitter_result.py
# @Author: Cedar
# @Date  : 2020/10/14
# @Desc  :


from requests.adapters import HTTPAdapter
import json
from lxml import etree
import requests
import datetime
import time
from urllib.parse import quote
import random


def get_token():
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    url = "http://107.180.91.218:5200/cloud_service/twitter/get_guest_token"
    response = s.get(url=url, timeout=30).text
    token_list = json.loads(response)
    return token_list


def get_twitter_list(url, token, proxies=None):
    headers = {
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "referer": "https://twitter.com/KlayThompson",
        "origin": "https://twitter.com",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "x-guest-token": token,
        "accept": "*/*",
        "accept-encodin": "gzip, deflate, br",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors"

    }
    text = ''
    for i in range(3):
        try:
            response = requests.get(url, proxies=proxies, headers=headers, timeout=20)
            response.encoding = 'utf-8'
            text = response.text
            if len(text) > 0:
                break
        except Exception as e:
            print(str(e))
            continue

    return text


def parse_html(text):
    """
    解析获取到的message_html源码，提取必须字段，索引至ES
    :return:
    """
    tweets_list = []
    json_data = json.loads(text)
    tweets = json_data["globalObjects"]["tweets"]
    users = json_data["globalObjects"]["users"]
    try:
        next_cursor = \
        json_data["timeline"]['instructions'][0]['addEntries']['entries'][-1]["content"]["operation"]["cursor"]["value"]
    except:
        next_cursor = ""

    for tweet in tweets.values():
        data = {}
        author_id = tweet["user_id_str"]
        data['author_id'] = author_id
        data['author_account'] = users[author_id]["screen_name"]
        data['author_name'] = users[author_id]["name"]
        data['author_url'] = f"https://twitter.com/{data['author_account']}"
        data['author_img_url'] = users[author_id]["profile_image_url_https"]
        data['article_url'] = f"https://twitter.com/{data['author_account']}/status/{tweet['id_str']}"
        created_at = time.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y")
        data['article_pubtime'] = time.strftime("%Y-%m-%d %H:%M:%S", created_at)
        data['article_content'] = tweet["full_text"]
        # article_content = clean_html_attr(article_content)  # html清洗
        tweets_list.append(data)

    return [next_cursor, tweets_list]


def get_tweet(url, page_count, proxies=None):
    results = []
    try:
        url_prefix = url
        token_list = []
        # 同时请求本地和云上的token，将本地token放在最后，优先使用
        cloud_token = get_token()
        token_list.extend(cloud_token)
        # 打乱顺序
        random.shuffle(token_list)
        token = token_list.pop()

        for i in range(page_count):
            print(url)
            # 依据当前token个数进行重试
            for j in range(len(token_list)):
                source = get_twitter_list(url, token, proxies)
                json_data = json.loads(source)
                if "errors" in json_data:
                    error_code = json_data["errors"][0]["code"]
                    if error_code == 200:
                        print(f"no{j}token{token} has expire")
                        token = token_list.pop()
                    elif error_code == 88:
                        print(f"no{j}token{token} is not valid for now")
                        token = token_list.pop()
                    elif error_code == 22:
                        print("it's a private account")
                        break
                    else:
                        # print(json_data)
                        break
                else:
                    break
            if "errors" not in json_data:
                page_content = parse_html(source)
                next_cursor = page_content[0]
                tweets_list = page_content[1]
                results = results + tweets_list
                print(results)
                if len(results) == 0:
                    if i == 0:
                        print("no post for this account")
                    break
                if next_cursor:
                    if len(next_cursor) > 0:
                        next_cursor = quote(next_cursor)
                        url = f"{url_prefix}&cursor={next_cursor}"
                    else:
                        print("no next page")
                        break
                else:
                    break
            else:
                print("all token expire!")
                break
    except Exception as e:
        print(str(e))

    return results


def main():
    url = 'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=%40billgates&count=20&query_source=typeahead_click&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel'
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
