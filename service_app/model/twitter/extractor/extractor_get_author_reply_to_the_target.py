#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_author_reply_to_the_target.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import html
import json
from service_app.model.twitter.extractor.lib.get_author_profile import get_author_profile
from service_app.model.twitter.extractor.lib.get_twitter_result import get_tweet_or_user


def extractor_get_author_reply_to_the_target(target_account, proxies=None, page_count=1, html_code='0'):

    target_profile = []
    target_account_profile = get_author_profile(target_account, proxies)
    if target_account_profile:
        target_profile.append(target_account_profile)

    q = '(to%3A' + target_account + ')%20-filter%3Alinks%20filter%3Areplies'
    url = 'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=' + q + '&count=20&query_source=typeahead_click&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel'
    author_list = []
    error = None
    try:
        # 假如get_tweet返回的值不是list，会报错，说明内容不对，进入except提示
        author_list = [] + get_tweet_or_user(url, page_count, proxies)
        status = '1'

    except Exception as e:
        status = '0'
        error = str(e)
        print(e)

    # 输出结果为json
    result = {"status": status, "error": error, "agent_type": "twitter", "fetch_type": "get_author_reply_to_the_target", "target_profile": target_profile,
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
    target_account = 'BBC'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_get_author_reply_to_the_target(target_account, proxies)
    print(result)


if __name__ == '__main__':
    main()
