#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_tweet_of_suspended_author.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import requests
from requests.adapters import HTTPAdapter
from lxml import etree
import html
import json


def fetch_author_profile(root):
    """
    获取target profile字段信息
    :param root: 输入为etree.HTML()对象
    :return: profile dict
    """
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

    try:
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


def extractor_get_tweet_of_suspended_author(target_account, proxies, html_code='0'):
    headers = {
        'Host': 'web.archive.org',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    # 这里日期写20即可，网站会自动去获取最新一次的镜像
    url = 'https://web.archive.org/web/20/https://twitter.com/' + target_account
    # url = 'https://web.archive.org/web/20191206212201/https://twitter.com/M7MD_SHAMRANI'
    author_list = []
    target_profile = []
    status = '0'
    try:
        # print('--------------1---------------')
        # requests 重试机制
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        response = s.get(url, headers=headers, timeout=30, allow_redirects=True, proxies=proxies)
        response.encoding = "utf-8"
        # 请求成功时就把status置为1,不管后面是否有数据
        if response.content:
            status = '1'
        root = etree.HTML(response.content, parser=etree.HTMLParser(encoding='utf-8'))
        items = root.xpath('//li[@data-item-type="tweet"]')

        # 到这里可能会因为账户suspended，所以会跳转到已suspended的页面，
        # https://web.archive.org/web/20191206214616/https://twitter.com/account/suspended
        # 需要进行搜索，找到最近的有数据的镜像
        if len(items) == 0:
            search_url = 'https://web.archive.org/__wb/sparkline?url=https%3A%2F%2Ftwitter.com%2F' + target_account + '&collection=web&output=json'
            search_response = requests.get(search_url, headers=headers, timeout=30, allow_redirects=True, proxies=proxies)
            search_response_json = search_response.json()
            last_ts = search_response_json["last_ts"]
            url = 'https://web.archive.org/web/' + last_ts + '/https://twitter.com/' + target_account
            # 请求最终数据
            # print('--------------2---------------')
            response = requests.get(url, headers=headers, timeout=30, allow_redirects=True, proxies=proxies)
            response.encoding = "utf-8"
            root = etree.HTML(response.content, parser=etree.HTMLParser(encoding='utf-8'))
            items = root.xpath('//li[@data-item-type="tweet"]')

        # 获取target profile
        target_profile = []
        target_account_profile = fetch_author_profile(root)
        if target_account_profile:
            target_profile.append(target_account_profile)

        # 解析数据到具体字段
        for item in items:
            # 不要写item.xpath('.//a[@class="person_link"]/text()')[0]，有可能导致list out of index
            # author
            author_id = "".join(item.xpath('.//div/@data-user-id'))
            author_account = "".join(item.xpath('.//div/@data-screen-name'))
            author_name = "".join(item.xpath('.//div/@data-name'))
            author_url = "https://twitter.com/" + author_account
            author_img_url = "".join(item.xpath('.//img[@class="avatar js-action-profile-avatar"]/@src'))
            author_description = "".join(item.xpath('//p[@class="ProfileHeaderCard-bio u-dir"]/text()'))
            author_follower_count = "".join(item.xpath('//a[@data-nav="followers"]/span[@data-count]/@data-count'))
            author_following_count = "".join(item.xpath('//a[@data-nav="following"]/span[@data-count]/@data-count'))
            author_message_count = "".join(item.xpath('//a[@data-nav="tweets"]/span[@data-count]/@data-count'))
            author_like_count = "".join(item.xpath('//a[@data-nav="favorites"]/span[@data-count]/@data-count'))
            # article
            article_url = "https://twitter.com" + "".join(item.xpath('.//div/@data-permalink-path'))
            article_pubtime = "".join(item.xpath('.//span[@data-time]/@data-time'))
            article_reply_count = "".join(item.xpath('.//button[contains(@class,"js-actionReply")][1]'
                                                     '//span[@class="ProfileTweet-actionCountForPresentation"]/text()'))
            article_retweet_count = "".join(item.xpath('.//button[contains(@class,"js-actionRetweet")][1]'
                                                       '//span[@class="ProfileTweet-actionCountForPresentation"]/text()'))
            article_favorite_count = "".join(item.xpath('.//button[contains(@class,"js-actionFavorite")][1]'
                                                        '//span[@class="ProfileTweet-actionCountForPresentation"]/text()'))
            article_content_text = item.find('.//div[@class="js-tweet-text-container"]')
            article_content_media = item.find('.//div[@class="AdaptiveMediaOuterContainer"]')
            article_content_quote = item.find('.//div[@class="QuoteTweet-container"]')
            article_content_text = etree.tostring(article_content_text)  # 转为bytes
            article_content_text = str(article_content_text, encoding="utf-8")  # 转为字符串
            article_content = article_content_text
            if article_content_media is not None:
                article_content_media = etree.tostring(article_content_media)  # 转为bytes
                article_content_media = str(article_content_media, encoding="utf-8")  # 转为字符串
                article_content = article_content + article_content_media
            if article_content_quote is not None:
                article_content_quote = etree.tostring(article_content_quote)  # 转为bytes
                article_content_quote = str(article_content_quote, encoding="utf-8")  # 转为字符串
                article_content = article_content + article_content_quote

            author_item = {
                "author_id": author_id,
                "author_account": author_account,
                "author_name": author_name,
                "author_url": author_url,
                "author_img_url": author_img_url,
                "author_description": author_description,
                "author_follower_count": author_follower_count,
                "author_following_count": author_following_count,
                "author_message_count": author_message_count,
                "author_like_count": author_like_count,
                "article_url": article_url,
                "article_pubtime": article_pubtime,
                "article_reply_count": article_reply_count,
                "article_retweet_count": article_retweet_count,
                "article_favorite_count": article_favorite_count,
                "article_content": article_content,
            }
            author_list.append(author_item)

    except Exception as e:
        status = str(e)
        print(e)

    result = {"status": status, "agent_type": "twitter", "fetch_type": "get_tweet_of_suspended_author", "target_profile": target_profile,
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
    proxies = {
        'http': 'http://127.0.0.1:4411',
        'https': 'http://127.0.0.1:4411'
    }
    target_account = 'M7MD_SHAMRANI'
    result = extractor_get_tweet_of_suspended_author(target_account, proxies)
    print(result)


if __name__ == '__main__':
    main()
