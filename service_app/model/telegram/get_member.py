
# 获取telegram 群成员数据的程序入口

import os
import html
import json
import random
from configparser import ConfigParser
from service_app.model.telegram.src.TelegramChannelMemberExtractor import TGMemExtractor


curpath = os.path.dirname(os.path.realpath(__file__))


def extractor_get_member(username, html_code='0'):
    status = '0'
    member_count = 0
    data_result = ''
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
        print(tg_session_name)
        config = {
            'TG_session_name': tg_session_name,
            'TG_api_id': TG_api_id,
            'TG_api_hash': TG_api_hash,
            'proxy_address': cfg.get('proxy', 'proxy_address'),
            'proxy_port': int(cfg.get('proxy', 'proxy_port') or 0),
            'group_member': os.path.join(curpath, cfg.get('download_addr', 'group_member')),
            'group_avatar': os.path.join(curpath, cfg.get('download_addr', 'group_avatar'))
        }
        # print(config)
        tg_mem_extrator = TGMemExtractor(config)
        flag = False
        tg_mem_extrator.set_channel(username)
        tg_mem_extrator.dump_to_json(flag)

        # 读取结果，返回
        file_name = username.lower() + ".json"
        member_file_name = os.path.join(curpath, "author", file_name)
        fl = open(member_file_name, 'r', encoding='utf-8')
        file_read = fl.read()
        if len(file_read) > 0:
            status = '1'

        file_read_json = json.loads(file_read)
        data_result = file_read_json['data']
        try:
            member_count = file_read_json['data']['group_member_count']

        except Exception as e:
            member_count = 1

        print(member_count)

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
