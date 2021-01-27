#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : controller.py
# @Author: Cedar
# @Date  : 2019/12/21
# @Desc  : Agent管理器，根据agent_type,分发任务给到不同Agent对象去执行


from service_app.model.twitter.twitter_agent import TwitterAgent
from service_app.model.telegram.telegram_agent import TelegramAgent
from service_app.model.breach.breach_agent import BreachAgent
from service_app.model.video_download.video_download_agent import VideoDownloadAgent
from service_app.model.match_account.match_account_agent import MatchAccountAgent
from service_app.model.facebook.facebook_agent import FacebookAgent
from service_app.model.instagram.instagram_agent import InstagramAgent
from service_app.model.vk.vk_agent import VkAgent


class FetchAgentManager:
    """
    Agent服务管理器，根据web请求的类型，来分发模块处理
    """

    def __init__(self, params):
        self.request_params = params

    def get_fetch_result_by_agent(self):

        cur_fetch_agent = None

        if self.request_params['agent_type'] == 'twitter':
            cur_fetch_agent = TwitterAgent(self.request_params)
        if self.request_params['agent_type'] == 'telegram':
            cur_fetch_agent = TelegramAgent(self.request_params)
        if self.request_params['agent_type'] == 'breach':
            cur_fetch_agent = BreachAgent(self.request_params)
        if self.request_params['agent_type'] == 'video_download':
            cur_fetch_agent = VideoDownloadAgent(self.request_params)
        if self.request_params['agent_type'] == 'match_account':
            cur_fetch_agent = MatchAccountAgent(self.request_params)
        if self.request_params['agent_type'] == 'facebook':
            cur_fetch_agent = FacebookAgent(self.request_params)
        if self.request_params['agent_type'] == 'instagram':
            cur_fetch_agent = InstagramAgent(self.request_params)
        if self.request_params['agent_type'] == 'vk':
            cur_fetch_agent = VkAgent(self.request_params)

        response = cur_fetch_agent.get_fetch_result()
        return response


if __name__ == '__main__':
    params = {
        'agent_type': 'video_download',
        'target_express': 'https://www.youtube.com/watch?v=qnaZm8JL5rE',
    }
    vv = FetchAgentManager(params)
    result = vv.get_fetch_result_by_agent()
    print(result)
