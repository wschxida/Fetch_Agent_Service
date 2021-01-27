#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_tweet_of_advanced_search.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :

import html
import json
from urllib.parse import quote
from service_app.model.twitter.extractor.lib.get_author_profile import get_author_profile
from service_app.model.twitter.extractor.lib.get_twitter_result import get_tweet_or_user


def extractor_get_tweet_of_advanced_search(query_dict='{}', proxies=None, page_count=1, html_code='0'):

    author_list = []
    target_profile = []
    error = None

    try:
        query_dict = json.loads(query_dict)
        # return query_dict

        # 规定输入参数
        query = {
            'words': '',
            'from_account': '',
            'min_replies': '',
            'min_faves': '',
            'min_retweets': '',
            'lang': '',
            'until': '',
            'since': '',
        }

        for i in query_dict.keys():
            query[i] = query_dict[i]

        q = ''
        if query['words']:
            q = q + query['words']
        if query['from_account']:
            q = q + ' (from:' + query['from_account'] + ')'
        if query['min_replies']:
            q = q + ' min_replies:' + query['min_replies']
        if query['min_faves']:
            q = q + ' min_faves:' + query['min_faves']
        if query['min_retweets']:
            q = q + ' min_retweets:' + query['min_retweets']
        if query['lang']:
            q = q + ' lang:' + query['lang']
        if query['until']:
            q = q + ' until:' + query['until']
        if query['since']:
            q = q + ' since:' + query['since']

        q = quote(q)
        url = 'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=' + q + '&count=20&query_source=typeahead_click&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel'

        if query['from_account']:
            target_account_profile = get_author_profile(query['from_account'], proxies)
            if target_account_profile:
                target_profile.append(target_account_profile)

        # 假如get_tweet返回的值不是list，会报错，说明内容不对，进入except提示
        search_result = [] + get_tweet_or_user(url, page_count, proxies)
        status = '1'

        # 按约定格式输出
        for item in search_result:
            author_item = {
                "author_id": "",
                "author_account": "",
                "author_name": "",
                "author_url": "",
                "author_img_url": "",
                "article_id": "",
                "article_url": "",
                "article_pubtime": "",
                "article_content": "",
                "reply_count": "",
                "retweet_count": "",
                "favorite_count": "",
            }
            author_item.update(item)
            author_item['article_id'] = author_item['article_url'].split('/status/')[1]
            author_list.append(author_item)

    except Exception as e:
        status = '0'
        error = str(e)
        print(e)

    # 输出结果为json
    result = {"status": status, "error": error, "agent_type": "twitter", "fetch_type": "get_tweet_of_advanced_search", "target_profile": target_profile,
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
    query_dict = '''{
      "words": "中国",
      "from_account": "VOAChinese",
      "min_replies": "15",
      "min_faves": "15",
      "min_retweets": "15",
      "lang": "zh-cn",
      "until": "2020-01-30",
      "since": "2018-12-22"
    }'''
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_get_tweet_of_advanced_search(query_dict, proxies)
    print(result)


if __name__ == '__main__':
    main()
