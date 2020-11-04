import socks
import json
import os
import parsedatetime
import datetime
import time
from telethon import TelegramClient


def get_timestamp(time_str):
    p = parsedatetime.Calendar()
    time_struct, parse_status = p.parse(time_str)
    datetime_result = datetime.datetime(*time_struct[:6])
    t = datetime_result.timetuple()
    result = time.mktime(t)
    return result


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
        if self.proxy_address:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash,
                                         proxy=(socks.HTTP, self.proxy_address, self.proxy_port))
        else:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

    def set_channel(self, username):
        self.channel_username = username

    def tg_login(self, config):
        session_name = config['TG_session_name']
        api_id = config['TG_api_id']
        api_hash = config['TG_api_hash']
        proxy_address = config['proxy_address']
        proxy_port = config['proxy_port']
        if proxy_address:
            self.client = TelegramClient(session_name, api_id, api_hash, proxy=(socks.HTTP, proxy_address, proxy_port))
        else:
            self.client = TelegramClient(session_name, api_id, api_hash)

    async def download_MsgPic(self,username,msg_id):
        path = ''
        try:
            chat_item = await self.client.get_entity(username)
        except ValueError:
            print("ValueError:No channel has\"", username, "\"as username")
            return path
        message = await self.client.get_messages(chat_item, ids=msg_id)
        # print(message)
        if message.media:
            path = await message.download_media(".\media")
        else:
            print("Message for ",msg_id," has no media to download")
        return path

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

            post_author = message.post_author
            author_account = chat_item.username
            author_name = chat_item.title
            # 群组的消息，没有post_author
            if not post_author:
                user = await self.client.get_entity(message.from_id)
                author_account = user.username
                author_name = str(user.first_name) + ' ' + str(user.last_name)

            has_media = False
            if message.media:
                has_media = True
                # path = await message.download_media(".\media")
                # print(path)
            msg = {
                "article_detail": {
                    "article_url": "https://t.me/" + self.channel_username + '/' + str(message.id),
                    "domain_code": "telegram.org",
                    "media_type_code": "c",
                    "author_name": author_name,
                    "author_account": author_account,
                    "article_pubtime_str": str(message.date),
                    "article_pubtime": message.date,
                    "article_title": message.message,
                    "article_HasMedia": has_media,
                    "message_id": message.id,
                },
                "article_application": {
                    "application_name": "Telegram",
                    "chat_group_name": chat_item.title,
                    "chat_group_account": chat_item.username,
                }
            }
            msg_dict.append(msg)
        print("get channel Message successfully")
        # print(msg_dict)
        os.makedirs(self.message_path, exist_ok=True)
        file = self.message_path + chat_item.username + ".json"
        # print(file)
        with open(file, "w") as f:
            json.dump(msg_dict, f, sort_keys=True, indent=4, separators=(',', ':'), default=str)
        # print("加载入文件完成...")

        return msg_dict

    def dump_to_json(self):
        with self.client:
            self.client.loop.run_until_complete(self.get_message())

    def download_message_media(self,username,id):
        with self.client:
            self.client.loop.run_until_complete(self.download_MsgPic(username=username,msg_id=id))