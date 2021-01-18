from locale import getdefaultlocale
import requests
import time
import sys
import os
import configparser
import random
from urllib.parse import quote
import json


def get_code_page():
    """
    Compatible with Linux and Windows
    :return:
    Linux:  ('en_US', 'UTF-8')
    Windows: ('zh_CN', 'cp936')
    """
    code_page = getdefaultlocale()[1]
    return code_page


def get_lines_from_file(file_path, remove_space_line=True):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'rb') as fp:
        content = fp.read().strip()
    try:
        content = content.decode('utf8')
    except Exception as e:
        content = content.decode(get_code_page())
    lines = content.splitlines()
    if remove_space_line:
        # 移除文件中的空行
        lines = [i for i in lines if i != '']
    return lines


def get_one_proxy(file_path='config/proxy_list.txt'):
    """
    随机取一个代理ip
    :param file_path:
    :return:一个代理ip
    """
    lines = get_lines_from_file(file_path)
    if lines is not None:
        if len(lines) > 0:
            proxy_ip = random.sample(lines, 1)
            return proxy_ip[0].strip()


def get_html(url, proxy=None, headers=None):
    proxies = {'http': None, 'https': None}
    if proxy is not None:
        proxy_ip = get_one_proxy()
        if proxy_ip is not None:
            proxies = {'http': f'http://{proxy_ip}', 'https': f'http://{proxy_ip}'}
    for i in range(3):
        try:
            response = requests.get(url, proxies=proxies, headers=headers, timeout=40).text
            return response
            break
        except Exception as e:
            print(str(e))
            continue


def get_twitter_list(url, token):
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
    response = get_html(url, proxy=1, headers=headers)
    return response


def save_to_file(*param):
    utc_time = int(time.time())
    website_no = param[0]
    output_dir = param[1]
    output_file = f"./output/{website_no}_{utc_time}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_dir)


def get_profile(requests_author_account, token):
    url = f"https://twitter.com/i/api/graphql/ZRnOhhXPwue_JGILb9TNug/UserByScreenName?variables=%7B%22screen_name%22%3A%22{requests_author_account}%22%2C%22withHighlightedLabel%22%3Atrue%7D"
    try:
        response = get_twitter_list(url, token)
        user_profile_dict = json.loads(response)["data"]["user"]["legacy"]
        user_profile_str = json.dumps(user_profile_dict)
        with open(profile_dir, 'w', encoding="utf-8") as f:
            f.write(user_profile_str)
    except Exception as e:
        print("get profile fail")
        print(str(e))


def parse_html(response, request_author_id, requests_author_account):
    """
    解析获取到的message_html源码，提取必须字段，索引至ES
    :return:
    """
    tweets_list = []
    json_data = json.loads(response)
    tweets = json_data["globalObjects"]["tweets"]
    users = json_data["globalObjects"]["users"]
    try:
        next_cursor = \
        json_data["timeline"]['instructions'][0]['addEntries']['entries'][-1]["content"]["operation"]["cursor"]["value"]
    except:
        next_cursor = ""

    for i in tweets.values():
        tweets_list.append(i)

    if len(tweets_list) == 0:
        print("no more post!")
    else:
        # 保存request account 的账号相关信息
        user_profile_dict = users[request_author_id]
        user_profile_str = json.dumps(user_profile_dict)
        with open(profile_dir, 'w', encoding="utf-8") as f:
            f.write(user_profile_str)

        for x in tweets_list:
            author_id = x["user_id_str"]
            full_text = x["full_text"]
            message_raw_id = x["id_str"]
            x["article_raw_id"] = message_raw_id
            if "retweeted_status_id_str" in x:
                continue
            if author_id != request_author_id:
                x["is_retweet"] = "1"
                x["original_author_id"] = author_id
                x["original_author_name"] = users[author_id]["name"]
                x["original_author_account"] = users[author_id]["screen_name"]
                x["avatar_img_url"] = users[author_id]["profile_image_url_https"]
                for k, v in tweets.items():
                    if "retweeted_status_id_str" in v:
                        if v['retweeted_status_id_str'] == message_raw_id:
                            x["article_raw_id"] = v["id_str"]
                            x["created_at"] = v["created_at"]
            created_at = time.strptime(x["created_at"], "%a %b %d %H:%M:%S %z %Y")
            x["article_pubtime"] = time.strftime("%Y-%m-%d %H:%M:%S", created_at)
            x["author_account"] = requests_author_account
            x["author_id"] = request_author_id
            if "extended_entities" in x:
                media_type = x["extended_entities"]["media"][0]["expanded_url"].split('/')[-2]
                if media_type == "video":
                    x["is_video"] = message_raw_id
                if media_type == "photo":
                    image_list = x["extended_entities"]["media"]
                    x["img_url"] = image_list[0]["media_url_https"]
                    image_l = []
                    for img in image_list:
                        image_l.append(img["media_url_https"])
                    x["image_list"] = "&".join(image_l)
            x["author_name"] = users[request_author_id]["name"]
            x["content_html"] = f'<div class="ib_text hilite_content">{full_text}</div>'
            del x["created_at"]
            del x["display_text_range"]
            del x["entities"]
            del x["user_id_str"]
            del x["full_text"]
            if "extended_entities" in x:
                del x["extended_entities"]
            str_json = json.dumps(x)
            with open(message_dir, 'a', encoding="utf-8") as f:
                f.write(str_json + '\r')
    return [next_cursor, tweets_list]


def get_id(account):
    author_id = ""
    url = f"http://{id_host}:{id_port}/service_app?agent_type=twitter&fetch_type=get_profile&target_express={request_account}"
    try:
        response = get_html(url, proxy=1)
        html = json.loads(response)
        author_id = html["target_profile"][0]["author_id"]
        file_name = f"./temp/{account}.id"
        with open(file_name, 'w') as f:
            f.write(author_id)
        return author_id
    except Exception as e:
        print("get author_id fail")
        print(str(e))
    return author_id


def get_token(proxy=None):
    try:
        proxies = {'http': None, 'https': None}
        if proxy is not None:
            proxy_ip = get_one_proxy()
            if proxy_ip is not None:
                proxies = {'http': f'http://{proxy_ip}', 'https': f'http://{proxy_ip}'}
        url = "https://api.twitter.com/1.1/guest/activate.json"
        headers = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        data = {}
        response = requests.post(url, proxies=proxies, data=data, headers=headers).text
        local_token = json.loads(response)["guest_token"]
        return local_token
    except Exception as e:
        print("get token fail!")
        print(str(e))


def get_token_by_cloud():
    cloud_token_list = []
    url = get_token_url
    try:
        response = get_html(url, proxy=token_proxy)
        cloud_token_list = json.loads(response)
    except Exception as e:
        print("get token list fail!")
        print(str(e))
    return cloud_token_list


def delete_token(guest_token):
    url = f"http://{token_host}:{token_port}/cloud_service/twitter/del_guest_token/{guest_token}"
    response = get_html(url, proxy=token_proxy)
    print(response)


def get_tweet(url, page_count, author_id, author_account):
    try:
        request_author_id = author_id
        url_prefix = url

        token_list = []
        # 同时请求本地和云上的token，将本地token放在最后，优先使用
        local_token = get_token(proxy=1)
        cloud_token = get_token_by_cloud()
        token_list.extend(cloud_token)
        token_list.append(local_token)
        token = token_list.pop()

        print(f"total token count:{len(token_list)}")
        for i in range(page_count):
            print(url)
            # 依据当前token个数进行重试
            for j in range(len(token_list)):
                response = get_twitter_list(url, token)
                json_data = json.loads(response)
                if "errors" in json_data:
                    error_code = json_data["errors"][0]["code"]
                    if error_code == 200:
                        print(f"no{j}token{token} has expire")
                        delete_token(token)
                        token = token_list.pop()
                        # error_message = json_data["errors"][0]["message"]
                        # error_str = datetime.now().strftime(
                        #     "%Y-%m-%d %H:%M:%S") + f":token{token}不可用   " + error_message
                        # with open("record.txt", 'a') as fp:
                        #     fp.write(error_str + '\n')
                    elif error_code == 88:
                        print(f"no{j}token{token} is not valid for now")
                        token = token_list.pop()
                    elif error_code == 22:
                        print("it's a private account")
                        get_profile(author_account, token)
                        break
                    else:
                        print(json_data)
                        break
                else:
                    break
            if "errors" not in json_data:
                page_content = parse_html(response, request_author_id, author_account)
                next_cursor = page_content[0]
                tweets_list = page_content[1]
                if len(tweets_list) == 0:
                    if i == 0:
                        print("no post for this account")
                        get_profile(author_account, token)
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


def main():
    start_time = time.time()
    try:
        author_id = get_id(request_account)
        if author_id == "not exist":
            print("this account is not exist")
            user_profile_dict = {"account_status": "not exist"}
            user_profile_str = json.dumps(user_profile_dict)
            with open(profile_dir, 'w', encoding="utf-8") as f:
                f.write(user_profile_str)
        elif len(author_id) > 0:
            url = f"https://twitter.com/i/api/2/timeline/profile/{author_id}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=true&count=20&userId={author_id}&ext=mediaStats%2ChighlightedLabel"
            get_tweet(url, int(loop_count), author_id, request_account)
        else:
            print(f"id error:{author_id}")
    except Exception as e:
        print(str(e))
    print("spend time : %s" % (time.time() - start_time))


if __name__ == '__main__':
    config_file = "D:\KIS_Server\Extraction_Server\Configs\Fetch_Service.ini"
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")
    token_host = config.get("token", "host")
    token_port = config.get("token", "port")
    id_host = config.get("id", "host")
    id_port = config.get("id", "port")
    get_token_url = f"http://{token_host}:{token_port}/cloud_service/twitter/get_guest_token"
    # 判断token服务是否内网外网
    if "192.168" in token_host:
        token_proxy = None
    else:
        token_proxy = 1

    request_account = sys.argv[1]
    loop_count = sys.argv[2]
    # request_account = "ASJ_ZIPUP"
    # loop_count = 3
    message_dir = f"./temp/message/{request_account}.txt"
    profile_dir = f"./temp/profile/{request_account}.txt"
    main()
