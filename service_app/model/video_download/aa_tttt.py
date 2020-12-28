#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : aa_tttt.py
# @Author: Cedar
# @Date  : 2020/10/20
# @Desc  :

from service_app.model.video_download.extractor_youtube_dl import extractor_youtube_dl_def

# target_express = 'https://www.youtube.com/watch?v=qnaZm8JL5rE'   # youtube
# target_express = 'https://twitter.com/i/videos/tweet/1317908612962988033'     # 可以
# target_express = 'https://twitter.com/i/videos/tweet/1339375349289922561'     # 不可以，retweet
# target_express = 'https://twitter.com/SaudiCustoms/status/1339375349289922561'        # 不可以，retweet
# target_express = 'https://twitter.com/i/status/1339188780767596544'     # 可以，上面url的原tweet
target_express = 'https://twitter.com/i/status/1329792051832115201'

proxies = {
    'http': 'http://127.0.0.1:7777',
    'https': 'http://127.0.0.1:7777'
}
result = extractor_youtube_dl_def(target_express, proxies)
print(result)
