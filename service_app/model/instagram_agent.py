# encoding=utf-8

import configparser
import os
import random
import requests
from service_app.model.base import BasePageAgent

# 用os模块来读取
curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "config_param.ini")  # 读取到本机的配置文件
# 调用读取配置模块中的类
conf = configparser.RawConfigParser()
conf.read(cfgpath, encoding="utf-8")
# 调用get方法，然后获取配置的数据
config_message_url_pattern = conf.get("instagram", "message_url_pattern")
config_profile_url_pattern = conf.get("instagram", "profile_url_pattern")
config_proxylist = conf.get("proxy", "proxylist")
# 转成list
if config_proxylist:
    config_proxylist = config_proxylist.split("||")


def get_result_by_requests(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/72.0.3626.121 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Connection": "keep - alive",
    }
    if config_proxylist:

        # proxy根据全局参数里面的设置，随机选取一个
        index = random.randint(0, len(config_proxylist) - 1)
        proxies = {
            'http': "http://" + config_proxylist[index],
            'https': "http://" + config_proxylist[index]
        }
        response = requests.get(url, headers=headers, proxies=proxies)

    else:
        response = requests.get(url, headers=headers)

    response.encoding = "utf-8"
    text = response.text
    return text


class InstagramAgent(BasePageAgent):
    """
    instagram类，获取profile，message
    调用get_page_content_by_request可根据page_type返回相应结果
    """

    def __init__(self, params):
        BasePageAgent.__init__(self, params)
        print('----------IG-----------')
        print(self.__dict__)
        print('==========IG===========')

    def get_page_content_by_request(self):
        if self.page_type == 'profile':
            return self.get_page_content_profile()
        if self.page_type == 'message':
            return self.get_page_content_message()

    def get_page_content_profile(self):
        url = config_profile_url_pattern.format(target_account=self.target_account)
        result = get_result_by_requests(url)
        return result

    def get_page_content_message(self):
        url = config_message_url_pattern.format(target_id=self.target_id)
        result = get_result_by_requests(url)
        return result


# =============================================================================

def main():
    params = {
        'page_type': 'message',
        'target_id': 34
    }
    result = InstagramAgent(params).get_page_content_by_request()
    print(result)


if __name__ == '__main__':
    main()
