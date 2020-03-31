# 20191217
# made by YHM
# 获取telegram 群消息数据的程序入口
# 使用格式：
# 1.python.exe D:/code/telegram/get_message.py -u [username]
# 2.python.exe D:/code/telegram/get_message.py -i [filename]


from configparser import ConfigParser
from model.telegram.src.TelegramChannelMessageExtractor import TGMsgExtrator
import sys, getopt

def main(argv,tgMsgExtrator):
    inputfile = ''
    username = ''
    try:
        opts, args = getopt.getopt(argv,"hi:u:",["ifile=","uname="])
    except getopt.GetoptError:
        print('get_message.py -i <inputfile> -u <username>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('get_message.py -i <inputfile> -u <username>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            break
        elif opt in ("-u", "--uname"):
            username = arg
            break
    if inputfile != '' :
        f = open(inputfile, 'r')
        result = list()
        for line in f.readline():
            result.append(line)
            # username = 'JapaneseSpeaking'
            tgMsgExtrator.set_channel(line)
            tgMsgExtrator.dump_to_json()
        print("get",line)
        f.close()
    elif username != '':
        tgMsgExtrator.set_channel(username)
        tgMsgExtrator.dump_to_json()


cfg = ConfigParser()
cfg.read('./config/telegram_extractor.ini', encoding='utf-8')
config = {
    'msg_max_limit': int(cfg.get('message_lim', 'msg_max_limit')),
    'TG_session_name': cfg.get('login_setting', 'TG_session_name'),
    'TG_api_id': int(cfg.get('login_setting', 'TG_api_id')),
    'TG_api_hash': cfg.get('login_setting', 'TG_api_hash'),
    'proxy_address': cfg.get('login_setting', 'proxy_address'),
    'proxy_port': int(cfg.get('login_setting', 'proxy_port')),
    'group_message': cfg.get('download_addr', 'group_massage')
}
tgMsgExtrator = TGMsgExtrator(config)
main(sys.argv[1:],tgMsgExtrator)