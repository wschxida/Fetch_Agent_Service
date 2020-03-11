#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : twitter.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import random
from service_app.model.base.base_fetch_agent import BaseFetchAgent
from service_app.model.twitter.extractor_get_common_follower import extractor_get_common_follower
from service_app.model.twitter.extractor_get_common_following import extractor_get_common_following
from service_app.model.twitter.extractor_get_friend import extractor_get_friend
from service_app.model.twitter.extractor_get_author_mention_the_target import extractor_get_author_mention_the_target
from service_app.model.twitter.extractor_get_author_reply_to_the_target import extractor_get_author_reply_to_the_target
from service_app.model.twitter.extractor_get_author_retweet_the_target_tweet import extractor_get_author_retweet_the_target_tweet
from service_app.model.twitter.extractor_get_deleted_tweet import extractor_get_deleted_tweet
from service_app.model.twitter.extractor_get_tweet_of_suspended_author import extractor_get_tweet_of_suspended_author


class TwitterAgent(BaseFetchAgent):
    """
    twitter类
    调用get_fetch_result可根据fetch_type返回相应结果
    """

    def __init__(self, params):
        # 初始化积累参数
        BaseFetchAgent.__init__(self, params)

        # 取出config，自己需要的参数
        self.proxies = None
        self.user_data_dir_list = self.config.get("chromedriver", "user_data_dir")    # chrome可以设置多个用户目录,各自互不干扰
        # 转成list
        if self.user_data_dir_list:
            self.user_data_dir_list = self.user_data_dir_list.split("||")
        config_proxylist = self.config.get("proxy", "proxylist")
        # 转成list
        if config_proxylist:
            config_proxylist = config_proxylist.split("||")
            # proxy根据全局参数里面的设置，随机选取一个
            index = random.randint(0, len(config_proxylist) - 1)
            self.proxies = {
                'http': "http://" + config_proxylist[index],
                'https': "http://" + config_proxylist[index]
            }

        print('----------TW-----------')
        print(self.__dict__)
        print('==========TW===========')

    def get_fetch_result(self):
        if self.fetch_type == 'get_common_follower':
            return extractor_get_common_follower(self.target_list, self.proxies, self.page_count)
        if self.fetch_type == 'get_common_following':
            return extractor_get_common_following(self.target_list, self.proxies, self.page_count)
        if self.fetch_type == 'get_friend':
            return extractor_get_friend(self.target_express, self.proxies, self.page_count)
        if self.fetch_type == 'get_author_mention_the_target':
            return extractor_get_author_mention_the_target(self.target_express, self.proxies, self.page_count)
        if self.fetch_type == 'get_author_reply_to_the_target':
            return extractor_get_author_reply_to_the_target(self.target_express, self.proxies, self.page_count)
        if self.fetch_type == 'get_author_retweet_the_target_tweet':
            return extractor_get_author_retweet_the_target_tweet(self.target_express, self.user_data_dir_list)
        if self.fetch_type == 'get_deleted_tweet':
            return extractor_get_deleted_tweet(self.target_express, self.proxies, self.page_count)
        if self.fetch_type == 'get_tweet_of_suspended_author':
            return extractor_get_tweet_of_suspended_author(self.target_express, self.proxies)
