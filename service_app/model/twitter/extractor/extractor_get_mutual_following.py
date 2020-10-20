#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_mutual_following.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import html
import json
from service_app.model.twitter.extractor.lib.get_author_profile import get_author_profile
from service_app.model.twitter.extractor.lib.get_common_friend_by_twiangulate import get_common_friend_by_twiangulate


def extractor_get_mutual_following(target_list, user_data_dir_list, proxies=None, html_code='0'):
    target_profile = []
    author_list = []
    error = None
    try:
        # 获取profile
        target_account_list = target_list.split(",")
        for target_account in target_account_list:
            target_account_profile = get_author_profile(target_account, proxies)
            if target_account_profile:
                target_profile.append(target_account_profile)

        # 构造url
        url_account = '-'.join(target_account_list)
        url = 'http://www.twiangulate.com/search/' + url_account + '/common_friends/table/my_friends-1/'
        # url = 'http://www.twiangulate.com/search/anthonychao-David_P_Mullins/common_friends/table/my_friends-1/'
        user_data_dir = user_data_dir_list[0]
        # 假如返回的值不是list，会报错，说明内容不对，进入except提示
        author_list = [] + get_common_friend_by_twiangulate(url, user_data_dir)
        status = '1'

    except Exception as e:
        status = '0'
        error = str(e)
        print(e)

    result = {"status": status, "error": error, "agent_type": "twitter", "fetch_type": "get_mutual_following", "target_profile": target_profile,
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
    target_list = 'BillGates,BillClinton'
    user_data_dir_list = ['E:\\selenium\\AutomationProfile1']
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_get_mutual_following(target_list, user_data_dir_list, proxies)
    print(result)


if __name__ == '__main__':
    main()
