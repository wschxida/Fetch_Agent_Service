#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :

import os
import html
import json


curpath = os.path.dirname(os.path.realpath(__file__))


def extractor_get_member(username, html_code='0'):
    status = '0'
    member_count = 0
    data_result = ''
    try:
        cmd = f'''python3 {curpath}/os_system_run.py get_member {username}'''
        os.system(cmd)
        # 读取结果，返回
        file_name = os.path.join(curpath, "author", username.lower() + ".json")
        fl = open(file_name, 'r', encoding='utf-8')
        file_read = fl.read()
        if len(file_read) > 0:
            status = '1'

        file_read_json = json.loads(file_read)
        data_result = file_read_json['data']
        try:
            member_count = file_read_json['data']['group_member_count']

        except Exception as e:
            member_count = 1

    except Exception as e:
        status = str(e)
        print(e)

    result = {"status": status, "agent_type": "telegram", "fetch_type": "get_member",
              "data_item_count": member_count, "data": data_result}
    json_result = json.dumps(result, ensure_ascii=False)
    # 为了在线显示图片
    json_result = json_result.replace('/home/kismanager/KIS/Fetch_Agent_Service/service_app',
                                      '/img')

    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
    if html_code == '1':
        return html_result
    else:
        return json_result


def main():
    # username = 'drafts4'    # group
    username = 'aboutipad'  # group
    # username = 'tieliu'  # channel
    # username = '1306732370'
    result = extractor_get_member(username)
    print(result)


if __name__ == '__main__':
    main()
