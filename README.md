# Fetch Agent Service

##概述
Fetch_Agent_Service将是下一个版本的KIS甚至KWM中的重要组件，用于完成实时信息前端采集，方便后端采集软件WMT配置或者PHP或者Python获取后加工入库或展示。
犹如现在的Social_Agent_Service，未来可能要取代Social_Agent_Service或把Social_Agent_Service吸收为一个子模块

##功能
提供采集所需要的各种HTML代码，JSON代码，将外部采集的复杂性封装起来

##原理``````
统一入口，利用不同的子目录用不同的python代码实现，然后通过指定action与其它参数来调用

##框架
Flask

##代码
每个功能子目录的框架都一样，都从一个基类集成，基类完成参数获取与结果返回，每个子目录调用python代码完成采集，实现do_action函数

## 应用模式：
[请求数据] -> [flask收到请求] -> [后台采用requests、selenium等采集数据] -> [web返回]

## 全局参数
config_param.ini
```
;多个值用||隔开

[scroll]
total_scrolls_default=5
;等待时间
scroll_time=10

[proxy]
proxylist=127.0.0.1:7777

[login]
;账号顺序要与chromedriver目录顺序一致
facebook_email_password={"email": "hlf35545@bcaoo.com", "password": "uh591g26*G"}||{"email": "cjt28336@bcaoo.com", "password": "CJT@283#36$"}

[chromedriver]
;账号顺序要与chromedriver目录顺序一致
user_data_dir=E:\selenium\AutomationProfile1||E:\selenium\AutomationProfile2

[instagram]
message_url_pattern=https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables=%7B%22id%22%3A%22{target_id}%22%2C%22first%22%3A50%2C%22after%22%3A%22%22%7D
profile_url_pattern=https://www.instagram.com/{target_account}/

[facebook]
profile_url_pattern=https://www.facebook.com/{target}
message_url_pattern=https://www.facebook.com/{target}
friend_url_pattern=https://www.facebook.com/{target}
```

## 接口格式
* action：获取类型
* website_code：网站类型，目前可选instagram、facebook，小写。（后期再支持其他类型）
* target_account：account
* target_id：id
* page_type：要获取的作者的数据类型，目前可选profile、message、friend小写。
* page_count：翻页页数
* url：url


###接口示例

```
模式：
Fetch_Agent_Service?action=fetch_social_page_html&website_code=facebook&target_account=bill.filip.5&page_type=message&page_count=5
Fetch_Agent_Service?action=fetch_social_page_html&website_code=xy&target_id=123456&page_type=message&page_count=5
Fetch_Agent_Service?action=fetch_any_page_html&url=news.google.com
Fetch_Agent_Service?action=fetch_twitter_id&target_account=abcd
Fetch_Agent_Service?action=fetch_skype_info&target_account=tom.jack

示例：
----------Instagram----------
Fetch Instagram Author Profile
http://127.0.0.1:5000/fetch_agent_service?action=fetch_social_page_html&website_code=instagram&page_type=profile&target_account=bill

target输入必须是account


Fetch Instagram Author Message
http://127.0.0.1:5000/fetch_agent_service?action=fetch_social_page_html&website_code=instagram&page_type=message&target_id=34&page_count=1

target输入必须是id, 目前还没支持翻页


----------Facebook----------
Fetch Facebook Author Profile
http://127.0.0.1:5000/fetch_agent_service?action=fetch_social_page_html&website_code=facebook&page_type=profile&target_account=bnbarry34

target输入可以是id也可以是account


Fetch Facebook Author Message
http://127.0.0.1:5000/fetch_agent_service?action=fetch_social_page_html&website_code=facebook&page_type=message&target_account=bnbarry34&page_count=1

target输入可以是id也可以是account


Fetch Facebook Author Friends
http://127.0.0.1:5000/fetch_agent_service?action=fetch_social_page_html&website_code=facebook&page_type=friend&target_account=bnbarry34&page_count=1

target输入可以是id也可以是account
```

## 程序设计
### Instagram
##### Fetch Instagram Author Profile
```
构造请求URL：
https://www.instagram.com/bill/
采用requests库，通用方法获取数据返回

def get_html_requests(url):
    ...
    # proxy根据全局参数里面的设置，随机选取一个
    response = requests.get(url, headers=headers, proxies=proxies)
```

##### Fetch Instagram Author Message
```
构造请求URL：
https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables=%7B%22id%22%3A%2234%22%2C%22first%22%3A50%2C%22after%22%3A%22%22%7D
采用requests库，通用方法获取数据返回
```

### Facebook
##### Fetch Instagram Author Message
```
构造请求URL：
https://www.facebook.com/bill.filip.5

采用selenium库。在本地构建多个Chrome的user_data_dir，每个user_data_dir之间互不干扰，
固定登录不同的Facebook账号，可人工维护。每次采集随机选取一个user_data_dir启动，不清理
缓存和cookie的情况下，可以保持登录而不需要重新安全码进行验证。可以达到在同一个服务器上自
动切换账号，分散请求压力的目的。

facebook_scraper.py

def scrap_message(url):
    ...
    # 随机取一个chromedriver目录，每个目录的Chromedriver是互相隔开的，登录不同的账号，每次启动随机分配
    index = random.randint(0, len(user_data_dir) - 1)
    user_data_dir_arg = r"user-data-dir=" + user_data_dir[index]
    options.add_argument(user_data_dir_arg)

每个user_data_dir所对应的账号是固定的，第一次需要人工登录，第一次登录时会有安全码，从原先
设备生成即可。人工登录完成后需要在config_param.ini里面设置账号所对应的目录，顺序要一致。
采集过程中如果遇到登录过期，或者账号退出的情况，只要不清缓存和cookie，程序会自动登录原先的
账号。

人工登录设置目录的方法：
chrome.exe --user-data-dir="E:\selenium\AutomationProfile1"

# 隐藏selenium特征
# https://blog.csdn.net/qq_26877377/article/details/83307208
# https://cloud.tencent.com/developer/news/383866
# https://blog.csdn.net/sinat_38682860/article/details/86221844
# http://www.pianshen.com/article/3903350108/
# 隐藏window.navigator.webdriver
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
```


chrome.exe --user-data-dir="C:\selenium\AutomationProfile4"