#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : --get_author_profile.py
# @Author: Cedar
# @Date  : 2020/4/7
# @Desc  :


import requests
from requests.adapters import HTTPAdapter
from lxml import etree


def get_str_btw(s, front, back):
    """
    获取两个字符串中间的子串
    :param s:
    :param front:
    :param back:
    :return:
    """
    par = s.partition(front)
    return (par[2].partition(back))[0][:]


def get_author_profile(target_account, proxies=None):
    author_profile_dict = {
        "author_id": "",
        "author_account": "",
        "author_name": "",
        "author_url": "",
        "author_img_url": "",
        "banner_img_url": "",
        "author_message_count": "",
        "author_following_count": "",
        "author_follower_count": "",
        # "author_list_count": "",
        "author_location": "",
        # "author_profile_location": "",
        "author_description": "",
        # "author_language": "",
        # "author_time_zone": "",
        # "author_is_protected": "",
        # "author_is_verified": "",
        # "author_is_geo_enabled": "",
        "author_account_created_time": "",
        "author_homepage_url": "",
    }
    # url = 'https://mobile.twitter.com/' + target_account + '?lang=en'
    url = 'http://gettwitterid.com/?user_name=' + target_account + '&submit=GET+USER+ID'

    headers = {
        'Host': 'gettwitterid.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }

    try:
        # requests 重试机制
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        response = s.get(url, timeout=30, headers=headers, proxies=proxies)
        response.encoding = "utf-8"
        # print(response.text)
        root = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))

        # 不要写item.xpath('.//a[@class="person_link"]/text()')[0]，有可能导致list out of index
        root_text = "".join(root.xpath('.//table[@class="profile_info"]//p/text()')) + '$'
        # print(root_text)
        author_profile_dict["author_id"] = get_str_btw(root_text, 'Twitter User ID:', 'Full Name:')
        author_profile_dict["author_account"] = get_str_btw(root_text, 'Screen Name:', 'Total Followers:')
        author_profile_dict["author_name"] = get_str_btw(root_text, 'Full Name:', 'Screen Name:')
        if len(author_profile_dict["author_account"]) > 0:
            author_profile_dict["author_url"] = "https://twitter.com/" + author_profile_dict["author_account"]
        author_profile_dict["author_img_url"] = "".join(root.xpath('.//div[@id="profile_photo"]/img/@src'))
        author_profile_dict["banner_img_url"] = ''
        author_profile_dict["author_message_count"] = get_str_btw(root_text, 'Total Statuses:', '$')
        author_profile_dict["author_following_count"] = ''
        author_profile_dict["author_follower_count"] = get_str_btw(root_text, 'Total Followers:', 'Total Statuses:')
        author_profile_dict["author_location"] = ''
        author_profile_dict["author_description"] = ''
        author_profile_dict["author_account_created_time"] = ''
        author_profile_dict["author_homepage_url"] = ''

    except Exception as e:
        print(e)

    # if len(author_profile_dict["author_account"]) > 0:
    #     return author_profile_dict
    # else:
    #     return None
    return author_profile_dict


def main():
    target_account = 'BillGates'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = get_author_profile(target_account, proxies)
    print(result)


if __name__ == '__main__':
    main()



