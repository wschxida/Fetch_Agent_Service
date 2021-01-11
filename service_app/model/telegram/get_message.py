
import os
import html
import json
import random
from configparser import ConfigParser
from service_app.model.telegram.src.TelegramChannelMessageExtractor import TGMsgExtractor


curpath = os.path.dirname(os.path.realpath(__file__))


def extractor_get_message(username, html_code='0'):
    status = '0'
    message_count = 0
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
            'msg_max_limit': int(cfg.get('message_lim', 'msg_max_limit')),
            'TG_session_name': tg_session_name,
            'TG_api_id': TG_api_id,
            'TG_api_hash': TG_api_hash,
            'proxy_address': cfg.get('proxy', 'proxy_address'),
            'proxy_port': int(cfg.get('proxy', 'proxy_port') or 0),
            'group_message': os.path.join(curpath, cfg.get('download_addr', 'group_massage'))
        }

        tg_msg_extrator = TGMsgExtractor(config)
        tg_msg_extrator.set_channel(username)
        msg_return = tg_msg_extrator.dump_to_json()
        # print('msg_dict: ', msg_return)
        if 'ValueError' in msg_return:
            status = '1'
            message_count = 1
            data_result = msg_return
        else:
            # 读取结果，返回
            file_name = username + ".json"
            message_file_name = os.path.join(curpath, "message", file_name)
            fl = open(message_file_name, 'r', encoding='utf-8')
            file_read = fl.read()
            if len(file_read) > 0:
                status = '1'
            file_read_json = json.loads(file_read)
            data_result = file_read_json
            message_count = len(data_result)

    except Exception as e:
        status = str(e)
        print(e)

    result = {"status": status, "agent_type": "telegram", "fetch_type": "get_message",
              "data_item_count": message_count, "data": data_result}
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
    # username = 'tieliu'   # channel
    # username = 'misakatech' # channel
    # username = 'PublicTestGroup'  # group
    username = 'mogahed_1070'  # 错误的
    result = extractor_get_message(username)
    print(result)


if __name__ == '__main__':
    main()
