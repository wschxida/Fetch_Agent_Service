#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: Cedar
# @Date  : 2020/9/21
# @Desc  :

# encoding=utf-8

"""
Created on 2019年05月05日

@author: cedar
"""

from flask import Flask
from flask import request
import requests

app = Flask(__name__)


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Connection": "keep - alive",
    }
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    text = response.text

    return text


@app.route('/', methods=['GET', 'GET'])
def home():
    return '''
    <br>
    <p><h1><a href="article_content?agent_type=twitter&fetch_type=get_tweet_of_url&query_dict=%7B%22url%22%3A%22https%3A%2F%2Fmobile.twitter.com%22%7D%0D%0A">article_content</a></h1></p>
    '''


@app.route('/article_content', methods=['GET'])
def article_content():
    request_params = dict(request.args)
    return request_params


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5101)



