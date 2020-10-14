#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_author_mention_the_target.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import html
import json
from service_app.model.twitter.extractor.lib.get_author_profile import get_author_profile
from service_app.model.twitter.extractor.lib.get_mobile_twitter_result import get_tweet


def extractor_get_author_mention_the_target(target_account, proxies=None, page_count=1, html_code='0'):

    target_profile = []
    target_account_profile = get_author_profile(target_account, proxies)
    if target_account_profile:
        target_profile.append(target_account_profile)

    q = '(%40' + target_account + ')%20-filter%3Areplies%20-filter%3A(from%3A-' + target_account + ')%20'
    url = 'https://mobile.twitter.com/search?q=' + q + '&s=typd&x=20&y=24&f=live'
    author_list = []
    error = None
    try:
        # 假如get_tweet返回的值不是list，会报错，说明内容不对，进入except提示
        author_list = [] + get_tweet(url, page_count, proxies)
        status = '1'

    except Exception as e:
        status = '0'
        error = str(e)
        print(e)

    # 输出结果为json
    result = {"status": status, "error": error, "agent_type": "twitter", "fetch_type": "get_author_mention_the_target", "target_profile": target_profile,
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
    result = extractor_get_author_mention_the_target(target_account, proxies, 2)
    print(result)


if __name__ == '__main__':
    main()
