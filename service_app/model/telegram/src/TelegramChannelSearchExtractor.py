
# telegram group member extrator

import socks
import json
import os
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import ChannelInvalidError
from telethon.tl.types import Channel
from telethon.tl.types import ChannelParticipantsAdmins
from service_app.model.telegram.src.Enitity import memberEntity, groupEntity, channelEntity
from telethon.sync import TelegramClient
from telethon import functions, types
from configparser import ConfigParser



curpath = os.path.dirname(os.path.realpath(__file__))


class TGChannelSearcher(object):
    def __init__(self, config):
        self.session_name = config['TG_session_name']
        self.api_id = config['TG_api_id']
        self.api_hash = config['TG_api_hash']
        self.proxy_address = config['proxy_address']
        self.proxy_port = config['proxy_port']
        if self.proxy_address:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash,
                                         proxy=(socks.HTTP, self.proxy_address, self.proxy_port))
        else:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

    def search_channel(self, query_str):
        search_result = []
        with self.client as client:
            result = client(functions.contacts.SearchRequest(
                q=f'%{query_str}%',
                limit=100
            ))

            for item in result.chats:
                channel = channelEntity.channelEnitity()
                channel.initWithChannel(item)
                search_result.append(channel.__dict__)

            return search_result





