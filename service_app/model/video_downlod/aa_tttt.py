#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : aa_tttt.py
# @Author: Cedar
# @Date  : 2020/10/20
# @Desc  :

from model.video_downlod.extractor_youtube_dl import extractor_youtube_dl_def

target_express = 'https://www.youtube.com/watch?v=qnaZm8JL5rE'
proxies = {
    'http': 'http://127.0.0.1:7777',
    'https': 'http://127.0.0.1:7777'
}
result = extractor_youtube_dl_def(target_express, proxies)
print(result)
