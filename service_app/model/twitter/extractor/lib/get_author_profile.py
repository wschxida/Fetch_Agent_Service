#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : get_author_profile.py
# @Author: Cedar
# @Date  : 2020/4/7
# @Desc  :


import requests
import json
from requests.adapters import HTTPAdapter


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


def get_token():
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    url = "http://107.180.91.218:5200/cloud_service/twitter/get_guest_token"
    response = s.get(url=url, timeout=30).text
    token_list = json.loads(response)
    return token_list


def get_id_via_twitter(target_account, proxies):
    token_list = get_token()
    token = token_list.pop()
    for j in range(len(token_list) - 1):
        print(token)
        url = f"https://twitter.com/i/api/graphql/ZRnOhhXPwue_JGILb9TNug/UserByScreenName?variables=%7B%22screen_name%22%3A%22{target_account}%22%2C%22withHighlightedLabel%22%3Atrue%7D"
        header = {
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
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        response = s.get(url, headers=header,  proxies=proxies, timeout=40).text
        json_data = json.loads(response)
        if "errors" in json_data:
            if "data" in json_data:
                author_id = "not exist"
                break
            else:
                print("token不可用")
                token = token_list.pop()
        else:
            break
    if "errors" not in json_data:
        try:
            author_id = json.loads(response)["data"]["user"]["rest_id"]
        except:
            author_id = "not exist"
    print(author_id)
    return author_id


def get_author_profile(target_account, proxies=None):
    author_profile_dict = {
        "author_id": "",
        "author_account": "",
        # "author_name": "",
        # "author_url": "",
        # "author_img_url": "",
        # "banner_img_url": "",
        # "author_message_count": "",
        # "author_following_count": "",
        # "author_follower_count": "",
        # "author_list_count": "",
        # "author_location": "",
        # "author_profile_location": "",
        # "author_description": "",
        # "author_language": "",
        # "author_time_zone": "",
        # "author_is_protected": "",
        # "author_is_verified": "",
        # "author_is_geo_enabled": "",
        "author_account_created_time": "",
        "author_homepage_url": "",
    }
    # url = 'https://mobile.twitter.com/' + target_account + '?lang=en'
    # url = 'http://gettwitterid.com/?user_name=' + target_account + '&submit=GET+USER+ID'
    url = 'https://tweeterid.com/ajax.php'
    data = {"input": target_account}

    headers = {
        'Host': 'tweeterid.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://tweeterid.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Referer': 'https://tweeterid.com/',
        # 'Cookie': '__gads=ID=7d81d43d1c7779c2-22b955ab2bc50041:T=1607911005:RT=1607911005:S=ALNI_MbjCKAB44QGXXpRrDcW0TY-fWRm1A; __utmz=116903043.1607911007.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=116903043.358712375.1607911006.1607911006.1608272487.2; __utmc=116903043; __utmt=1; __utmb=116903043.2.10.1608272487',
    }

    try:
        # requests 重试机制
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        response = s.post(url=url, data=data, timeout=30, proxies=proxies, headers=headers)
        response.encoding = "utf-8"
        if response.text == "error":
            author_id = get_id_via_twitter(target_account, proxies)
            author_profile_dict["author_id"] = author_id
        else:
            author_profile_dict["author_id"] = response.text

        author_profile_dict["author_account"] = target_account
        # root = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))

        # 不要写item.xpath('.//a[@class="person_link"]/text()')[0]，有可能导致list out of index
        # root_text = "".join(root.xpath('.//table[@class="profile_info"]//p/text()')) + '$'
        # print(root_text)
        # author_profile_dict["author_id"] = get_str_btw(root_text, 'Twitter User ID:', 'Full Name:')
        # author_profile_dict["author_account"] = get_str_btw(root_text, 'Screen Name:', 'Total Followers:')
        # author_profile_dict["author_name"] = get_str_btw(root_text, 'Full Name:', 'Screen Name:')
        # if len(author_profile_dict["author_account"]) > 0:
        #     author_profile_dict["author_url"] = "https://twitter.com/" + author_profile_dict["author_account"]
        # author_profile_dict["author_img_url"] = ""
        # author_profile_dict["banner_img_url"] = ''
        # author_profile_dict["author_message_count"] = ''
        # author_profile_dict["author_following_count"] = ''
        # author_profile_dict["author_follower_count"] = ''
        # author_profile_dict["author_location"] = ''
        # author_profile_dict["author_description"] = ''
        # author_profile_dict["author_account_created_time"] = ''
        # author_profile_dict["author_homepage_url"] = ''

    except Exception as e:
        print(e)

    # if len(author_profile_dict["author_account"]) > 0:
    #     return author_profile_dict
    # else:
    #     return None
    return author_profile_dict


def main():
    target_account = 'Billgates'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = get_author_profile(target_account, proxies)
    print(result)


if __name__ == '__main__':
    main()



