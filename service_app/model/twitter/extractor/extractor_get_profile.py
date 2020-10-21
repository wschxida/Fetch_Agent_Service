#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_profile.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import html
import json
from model.twitter.extractor.lib.get_author_profile import get_author_profile


def extractor_get_profile(target_account, proxies=None, html_code='0'):
    try:
        target_profile = []
        target_account_profile = get_author_profile(target_account, proxies)
        if target_account_profile:
            target_profile.append(target_account_profile)
        status = '1'
        error = None
    except Exception as e:
        status = '0'
        error = str(e)
        target_profile = ''
        print(e)

    result = {"status": status, "error": error, "agent_type": "twitter", "fetch_type": "get_profile",
              "target_profile": target_profile, "data_item_count": 1, "data": ''}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
    if html_code == '1':
        return html_result
    else:
        return json_result


def main():
    target_list = 'BillGates'
    proxies = {
        'http': 'http://127.0.0.1:4411',
        'https': 'http://127.0.0.1:4411'
    }
    result = extractor_get_profile(target_list, proxies)
    print(result)


if __name__ == '__main__':
    main()
