
# 获取telegram 群成员数据的程序入口

import os
import html
import json
import random
from configparser import ConfigParser
from service_app.model.telegram.src.TelegramChannelSearchExtractor import TGChannelSearcher


curpath = os.path.dirname(os.path.realpath(__file__))


def extractor_search_channel(search_str, html_code='0'):
    status = '0'
    error = None
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

        tg_channel_searcher = TGChannelSearcher(config)
        data_result = tg_channel_searcher.search_channel(search_str)
        status = '1'
        # print(data_result)

    except Exception as e:
        status = '0'
        error = str(e)
        print(e)

    result = {"status": status, "error": error, "agent_type": "telegram", "fetch_type": "search_channel",
              "data_item_count": len(data_result), "data": data_result}
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
    search_str = 'daily'
    result = extractor_search_channel(search_str)
    print(result)


if __name__ == '__main__':
    main()
