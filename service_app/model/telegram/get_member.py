
# 获取telegram 群成员数据的程序入口

import os
from configparser import ConfigParser
from model.telegram.src.TelegramChannelMemberExtractor import TGMemExtrator


curpath = os.path.dirname(os.path.realpath(__file__))


def extractor_get_member(username):
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
    member_file_name = "./author/" + username + ".json"
    fl = open(member_file_name, 'r', encoding='utf-8')
    member_result = fl.read()
    return member_result


def main():
    username = 'Advancedchat'
    result = extractor_get_member(username)
    print(result)


if __name__ == '__main__':
    main()
