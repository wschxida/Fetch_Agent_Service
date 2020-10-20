#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_youtube_dl.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import html
import json
import youtube_dl


def extractor_youtube_dl(target_express, proxies=None, html_code='0'):
    data = ''
    status = '1'
    error = None
    try:

        # 定义某些下载参数
        ydl_opts = {
            'proxy': proxies['http'],
            'format': 'mp4',
            'retries': 10,
            'autonumber-start': 2,
            'ignore-errors': '',
            'skip_download': True,
        }

        # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #     y_dl_result = ydl.extract_info(video_url)
        #     print(y_dl_result)
        #     data = y_dl_result['url']
        #     print(data)
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        y_dl_result = ydl.extract_info(target_express)
        print(y_dl_result)
        data = y_dl_result['url']
        print(data)

    except Exception as e:
        status = '0'
        error = str(e)
        print(e)

    result = {"status": status, "error": error, "agent_type": "youtube-dl", "data": data}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
    if html_code == '1':
        return html_result
    else:
        return json_result


def main():
    target_express = 'https://www.youtube.com/watch?v=qnaZm8JL5rE'
    target_express = 'https://twitter.com/i/videos/tweet/1317908612962988033'
    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    result = extractor_youtube_dl(target_express, proxies)
    print(result)


if __name__ == '__main__':
    main()
