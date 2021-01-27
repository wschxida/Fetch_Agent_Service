
import html
import random
import socks
import json
import os
from telethon.sync import TelegramClient
from configparser import ConfigParser


curpath = os.path.dirname(os.path.realpath(__file__))


def extractor_get_profile(username, html_code='0'):
    target_profile = []
    status = '0'
    error = None

    try:
        cfg = ConfigParser()
        telegram_extractor_config_path = os.path.join(curpath, "./config/telegram_extractor.ini")
        cfg.read(telegram_extractor_config_path, encoding='utf-8')
        tg_session = cfg.get('login_setting', 'tg_session')
        tg_session_list = tg_session.split('||')
        # 随机选取一个session
        tg_session_choice = random.choice(tg_session_list).split(',')
        tg_session_name = os.path.join(curpath, 'config', tg_session_choice[0] + '.session')
        TG_api_id = int(tg_session_choice[1])
        TG_api_hash = tg_session_choice[2]
        config = {
            'TG_session_name': tg_session_name,
            'TG_api_id': TG_api_id,
            'TG_api_hash': TG_api_hash,
            'proxy_address': cfg.get('proxy', 'proxy_address'),
            'proxy_port': int(cfg.get('proxy', 'proxy_port') or 0),
            'group_member': os.path.join(curpath, cfg.get('download_addr', 'group_member')),
            'group_avatar': os.path.join(curpath, cfg.get('download_addr', 'group_avatar')),
            'channel_avatar': os.path.join(curpath, cfg.get('download_addr', 'channel_avatar'))
        }
        if config['proxy_address']:
            client = TelegramClient(config['TG_session_name'], config['TG_api_id'], config['TG_api_hash'],
                                         proxy=(socks.HTTP, config['proxy_address'], config['proxy_port']))
        else:
            client = TelegramClient(config['TG_session_name'], config['TG_api_id'], config['TG_api_hash'])

        with client:
            username_entity = client.get_entity(username)
            author_profile_dict = {
                "author_id": username_entity.id,
                "author_account": username_entity.username,
                "author_name": username_entity.title,
                "author_url": "https://t.me/" + username_entity.username,
            }
            target_profile.append(author_profile_dict)

        status = '1'

    except Exception as e:
        error = str(e)
        print(e)

    result = {"status": status, "error": error, "agent_type": "telegram", "fetch_type": "get_profile",
              "target_profile": target_profile, "data_item_count": 1, "data": ''}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
    if html_code == '1':
        return html_result
    else:
        return json_result


def main():
    # username = 'drafts4'    # group
    # username = 'aboutipad'  # group
    username = 'tieliu'  # channel
    # username = '1306732370'
    result = extractor_get_profile(username)
    print(result)


if __name__ == '__main__':
    main()
