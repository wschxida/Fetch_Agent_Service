import socks
import json
import os
from telethon import TelegramClient


class TGMsgExtrator:
    def __init__(self, config):
        self.msg_lim = config['msg_max_limit']
        self.session_name = config['TG_session_name']
        self.api_id = config['TG_api_id']
        self.api_hash = config['TG_api_hash']
        self.proxy_address = config['proxy_address']
        self.proxy_port = config['proxy_port']
        self.message_path = config['group_message']
        self.channel_username = ''
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash,
                                     proxy=(socks.HTTP, self.proxy_address, self.proxy_port))

    def set_channel(self, username):
        self.channel_username = username

    def TG_login(self, config):
        session_name = config['TG_session_name']
        api_id = config['TG_api_id']
        api_hash = config['TG_api_hash']
        proxy_address = config['proxy_address']
        proxy_port = config['proxy_port']
        self.client = TelegramClient(session_name, api_id, api_hash, proxy=(socks.HTTP, proxy_address, proxy_port))

    async def get_message(self):
        msg_dict = []
        try:
            chat_item = await self.client.get_entity(self.channel_username)
        except ValueError:
            print("ValueError:No channel has\"", self.channel_username, "\"as username")
            return msg_dict
        messages = self.client.iter_messages(chat_item, limit=self.msg_lim)
        async for message in messages:
            # print(message)
            # print(message.date, utils.get_display_name(message.sender), message.message)
            msg = {
                "article_detail": {
                    "article_url": "https://t.me/" + self.channel_username,
                    "domain_code": "telegram.org",
                    "media_type_code": "c",
                    "author_name": chat_item.title,
                    "author_account": chat_item.username,
                    "article_pubtime_str": str(message.date),
                    "article_pubtime": message.date.isoformat(timespec='microseconds'),
                    "article_title": message.message,
                },
                "article_application": {
                    "application_name": "Telegram",
                    "chat_group_name": chat_item.title
                }
            }
            msg_dict.append(msg)
        print("get channel Message successfully")
        # print(msg_dict)
        os.makedirs(self.message_path, exist_ok=True)
        file = self.message_path + chat_item.username + ".json"
        print(file)
        with open(file, "w") as f:
            json.dump(msg_dict, f, sort_keys=True, indent=4, separators=(',', ':'), default=str)
        print("加载入文件完成...")

        return msg_dict

    def dumpTojson(self):
        with self.client:
            self.client.loop.run_until_complete(self.get_message())
