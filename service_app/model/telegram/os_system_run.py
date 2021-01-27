#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/1/27
# @Desc  :


import os
import html
import json
import random
from configparser import ConfigParser
from telethon.sync import TelegramClient
from telethon import functions, types
import socks
import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), 'src'))
from TelegramChannelMemberExtractor import TGMemExtractor
from TelegramChannelMessageExtractor import TGMsgExtractor
from enitity import GroupEnitity, MessageEnitity, MemberEnitity, ChannelEnitity



cur_path = os.path.dirname(os.path.realpath(__file__))
cfg = ConfigParser()
telegram_extractor_config_path = os.path.join(cur_path, "./config/telegram_extractor.ini")
cfg.read(telegram_extractor_config_path, encoding='utf-8')
tg_session = cfg.get('login_setting', 'tg_session')
tg_session_list = tg_session.split('||')
# 随机选取一个session
tg_session_choice = random.choice(tg_session_list).split(',')
tg_session_name = os.path.join(cur_path, 'config', tg_session_choice[0] + '.session')
TG_api_id = int(tg_session_choice[1])
TG_api_hash = tg_session_choice[2]
config = {
    'TG_session_name': tg_session_name,
    'TG_api_id': TG_api_id,
    'TG_api_hash': TG_api_hash,
    'proxy_address': cfg.get('proxy', 'proxy_address'),
    'proxy_port': int(cfg.get('proxy', 'proxy_port') or 0),
    'group_member': os.path.join(cur_path, cfg.get('download_addr', 'group_member')),
    'group_avatar': os.path.join(cur_path, cfg.get('download_addr', 'group_avatar')),
    'channel_avatar': os.path.join(cur_path, cfg.get('download_addr', 'channel_avatar')),
    'msg_max_limit': int(cfg.get('message_lim', 'msg_max_limit')),
    'group_message': os.path.join(cur_path, cfg.get('download_addr', 'group_massage')),
}


def main(extract_type, username):
    if config['proxy_address']:
        client = TelegramClient(config['TG_session_name'], config['TG_api_id'], config['TG_api_hash'],
                                proxy=(socks.HTTP, config['proxy_address'], config['proxy_port']))
    else:
        client = TelegramClient(config['TG_session_name'], config['TG_api_id'], config['TG_api_hash'])

    if extract_type == 'get_member':
        tg_mem_extractor = TGMemExtractor(config)
        flag = False
        tg_mem_extractor.set_channel(username)
        tg_mem_extractor.dump_to_json(flag)

    if extract_type == 'get_message':
        tg_msg_extractor = TGMsgExtractor(config)
        tg_msg_extractor.set_channel(username)
        tg_msg_extractor.dump_to_json()

    if extract_type == 'search_channel':
        search_result = []
        with client as client:
            result = client(functions.contacts.SearchRequest(
                q=f'%{username}%',
                limit=100
            ))

            for item in result.chats:
                channel = ChannelEnitity()
                channel.initWithChannel(item)
                search_result.append(channel.__dict__)

        file = os.path.join(cur_path, 'author', username.lower() + "_search.json")
        with open(file, "w") as f:
            json.dump(search_result, f, sort_keys=True, indent=4, separators=(',', ':'), default=str)

    if extract_type == 'get_profile':
        target_profile = []
        with client:
            username_entity = client.get_entity(username)
            author_profile_dict = {
                "author_id": username_entity.id,
                "author_account": username_entity.username,
                "author_name": username_entity.title,
                "author_url": "https://t.me/" + username_entity.username,
            }
            target_profile.append(author_profile_dict)

        file = os.path.join(cur_path, 'author', username.lower() + "_profile.json")
        with open(file, "w") as f:
            json.dump(target_profile, f, sort_keys=True, indent=4, separators=(',', ':'), default=str)


if __name__ == '__main__':
    # print(sys.argv[1], sys.argv[2])
    main(sys.argv[1], sys.argv[2])
    # main('get_member', 'aboutipad')
    # main('get_profile', 'aboutipad')
