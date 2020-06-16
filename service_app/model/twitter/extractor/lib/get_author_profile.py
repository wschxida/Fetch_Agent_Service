#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : get_author_profile.py
# @Author: Cedar
# @Date  : 2020/4/7
# @Desc  :


import requests
from requests.adapters import HTTPAdapter
from lxml import etree


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
    url = 'https://twitter.com/' + target_account + '?lang=en'

    try:
        # requests 重试机制
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        response = s.get(url, timeout=30, proxies=proxies)
        response.encoding = "utf-8"
        print(response.text)
        root = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))

        # 不要写item.xpath('.//a[@class="person_link"]/text()')[0]，有可能导致list out of index
        author_profile_dict["author_id"] = "".join(root.xpath('.//div[@class="ProfileNav"]/@data-user-id'))
        author_profile_dict["author_account"] = "".join(root.xpath('.//div[@class="ProfileHeaderCard"]//span[@class="username u-dir"]/b/text()'))
        author_profile_dict["author_name"] = "".join(root.xpath('.//div[@class="ProfileHeaderCard"]//a[@class="ProfileHeaderCard-nameLink u-textInheritColor js-nav"]/text()'))
        if len(author_profile_dict["author_account"]) > 0:
            author_profile_dict["author_url"] = "https://twitter.com/" + author_profile_dict["author_account"]
        author_profile_dict["author_img_url"] = "".join(root.xpath('.//img[@class="ProfileAvatar-image "]/@src'))
        author_profile_dict["banner_img_url"] = "".join(root.xpath('.//div[@class="ProfileCanopy-headerBg"]/img/@src'))
        author_profile_dict["author_message_count"] = "".join(root.xpath('.//li[@class="ProfileNav-item ProfileNav-item--tweets is-active"]//span[@class="ProfileNav-value"]/@data-count'))
        author_profile_dict["author_following_count"] = "".join(root.xpath('.//li[@class="ProfileNav-item ProfileNav-item--following"]//span[@class="ProfileNav-value"]/@data-count'))
        author_profile_dict["author_follower_count"] = "".join(root.xpath('.//li[@class="ProfileNav-item ProfileNav-item--followers"]//span[@class="ProfileNav-value"]/@data-count'))
        author_profile_dict["author_location"] = "".join(root.xpath('.//div[@class="ProfileHeaderCard-location "]//a[@data-place-id]/text()'))
        author_profile_dict["author_description"] = "".join(root.xpath('.//p[@class="ProfileHeaderCard-bio u-dir"]/text()'))
        author_profile_dict["author_account_created_time"] = "".join(root.xpath('.//span[@class="ProfileHeaderCard-joinDateText js-tooltip u-dir"]/@title'))
        author_profile_dict["author_homepage_url"] = "".join(root.xpath('.//span[@class="ProfileHeaderCard-urlText u-dir"]//a[@class="u-textUserColor"]/@title'))

    except Exception as e:
        print(e)

    if len(author_profile_dict["author_account"]) > 0:
        return author_profile_dict
    else:
        return None


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



