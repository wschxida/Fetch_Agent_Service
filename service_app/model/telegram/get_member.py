#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_common_follower.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :

import os
import html
import json
from configparser import ConfigParser
from service_app.model.telegram.src.TelegramChannelMemberExtractor import TGMemExtrator


curpath = os.path.dirname(os.path.realpath(__file__))


def extractor_get_member(username):
    status = '0'
    member_count = 0
    data_result = ''
    try:
        cfg = ConfigParser()
        telegram_extractor_config_path = os.path.join(curpath, "./config/telegram_extractor.ini")
        cfg.read(telegram_extractor_config_path, encoding='utf-8')
        config = {
            'TG_session_name': cfg.get('login_setting', 'TG_session_name'),
            'TG_api_id': int(cfg.get('login_setting', 'TG_api_id')),
            'TG_api_hash': cfg.get('login_setting', 'TG_api_hash'),
            'proxy_address': cfg.get('login_setting', 'proxy_address'),
            'proxy_port': int(cfg.get('login_setting', 'proxy_port')),
            'group_member': cfg.get('download_addr', 'group_member'),
            'group_avatar': cfg.get('download_addr', 'group_avatar')
        }

        tg_mem_extrator = TGMemExtrator(config)
        flag = False
        tg_mem_extrator.set_channel(username)
        tg_mem_extrator.dump_to_json(flag)

        # 读取结果，返回
        file_name = username + ".json"
        member_file_name = os.path.join(curpath, "author", file_name)
        fl = open(member_file_name, 'r', encoding='utf-8')
        file_read = fl.read()
        if len(file_read) > 0:
            status = '1'

        file_read_json = json.loads(file_read)
        member_count = file_read_json['data']['group_member_count']
        data_result = file_read_json['data']
        print(member_count)

    except Exception as e:
        status = str(e)
        print(e)

    result = {"status": status, "agent_type": "telegram", "fetch_type": "get_member",
              "data_item_count": member_count, "data": data_result}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)

    return html_result


def main():
    username = 'drafts4'
    result = extractor_get_member(username)
    print(result)


if __name__ == '__main__':
    main()
