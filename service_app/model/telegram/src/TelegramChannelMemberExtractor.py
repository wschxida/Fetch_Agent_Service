
# telegram group member extrator

import socks
import json
import os
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import ChannelInvalidError
from telethon.tl.types import Channel
from telethon.tl.types import ChannelParticipantsAdmins
from service_app.model.telegram.src.Enitity import memberEntity, groupEntity


class TGMemExtrator(object):
    def __init__(self, config):
        self.session_name = config['TG_session_name']
        self.api_id = config['TG_api_id']
        self.api_hash = config['TG_api_hash']
        self.proxy_address = config['proxy_address']
        self.proxy_port = config['proxy_port']
        self.group_username = ''
        self.member_path = config['group_member']
        self.group_avatar_path = config['group_avatar']
        if self.proxy_address:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash,
                                         proxy=(socks.HTTP, self.proxy_address, self.proxy_port))
        else:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

    # 设置需要采集的telegram group username
    def set_channel(self, username):
        self.group_username = username

    # 换账号连接
    def TG_login(self, config):
        session = config['TG_session_name']
        api_id = config['TG_api_id']
        api_hash = config['TG_api_hash']
        proxy_address = config['proxy_address']
        proxy_port = config['proxy_port']
        if proxy_address:
            self.client = TelegramClient(session, api_id, api_hash, proxy=(socks.HTTP, proxy_address, proxy_port))
        else:
            self.client = TelegramClient(session, api_id, api_hash)

    # 指定user，下载头像
    async def download_profile_pic(self, username):
        # 根据username获取group的实体
        try:
            chat_item = await self.client.get_entity(username)
        except ValueError:
            print("ValueError:No group has\"", self.group_username, "\"as username")
            return None
        # 下载图片
        other = self.group_avatar_path + "\other"
        os.makedirs(other)
        if chat_item.photo is not None:
            data = await self.client.download_profile_photo(chat_item, file=other)
        else:
            data = None
        return data

    # 将采集的User信息转换成系统自定义的实体类处理
    def user_to_member_entity(self, user, pic_addr, admins):
        # 提取username，name
        member = memberEntity.memberEnitity()
        member.initWithUser(user)

        for i in range(admins.__len__()):
            if admins[i] == id:
                member.set_adminInfo(True)

        member.set_ProfilePic(pic_addr)
        return member

    # 获取群管理员的id
    async def get_group_administrator(self):
        admin_ids = []
        # 根据username获取group的实体
        try:
            chat_item = await self.client.get_entity(self.group_username)
        except ValueError:
            print("ValueError:No group has\"", self.group_username, "\"as username")
            return admin_ids
        # 判断实体为channel返回空数据，实体为user返回空数据，实体为group继续执行下面代码
        if isinstance(chat_item, Channel):
            if chat_item.megagroup is False:
                print("ValueError:its a channel ,cant get chaneel members without admin privileges")
                return admin_ids
        else:
            print("ValueError:its a User ,cant get a User's members")
            return admin_ids

        # 获取group的管理员
        admins = self.client.iter_participants(chat_item, filter=ChannelParticipantsAdmins)
        i = 0
        admin_ids = []
        async for admin in admins:
            admin_ids.append(admin.id)
            i += 1

        return admin_ids

    # 获取telegram group member 接口
    async def get_group_member(self, download_pic_flag):
        # 根据username获取group的实体
        try:
            chat_item = await self.client.get_entity(self.group_username)
        except ValueError:
            print("ValueError:No group has\"", self.group_username, "\"as username")
            return
        # 判断实体为channel返回空数据，实体为user返回空数据，实体为group继续执行下面代码
        if isinstance(chat_item, Channel):
            if chat_item.megagroup is False:
                print("ValueError:its a channel ,cant get chaneel members without admin privileges")
                return
        else:
            print("ValueError:its a User ,cant get a User's member")
            return
        # 获取group的全部成员
        participants = await self.client.get_participants(chat_item, aggressive=True)
        # 获取group的管理员
        admins = self.client.iter_participants(chat_item, filter=ChannelParticipantsAdmins)
        i = 0
        admin_ids = []
        async for admin in admins:
            admin_ids.append(admin.id)
            i += 1

        # 获取群成员
        path = (self.group_avatar_path+chat_item.username).strip()
        os.makedirs(path,exist_ok=True)
        group_avatar = await self.client.download_profile_photo(chat_item, file=path)
        group = groupEntity.groupEnitity()
        group.initWithGroup(chat_item)
        group.set_Member_Account(participants.total)
        if group_avatar:
            group.set_Avatar(self.group_avatar_path, group_avatar)

        mem_file_path = self.member_path + chat_item.username + ".json"
        result = {"data": ""}
        for user in participants:
            # 下载图片
            addr = None
            if download_pic_flag:
                try:
                    if user.photo is not None:
                        addr = await self.client.download_profile_photo(user, file=path)
                        # print(addr)
                except ChannelInvalidError:
                    print("download error")
            # 获取群成员信息
            mem = self.user_to_member_entity(user, addr, admin_ids)
            group.add_Member(mem.__dict__)

        result["data"] = group.__dict__
        # 将最后结果写到指定文件下
        with open(mem_file_path, "w") as f:
            json.dump(result, f, sort_keys=True, indent=4, separators=(',', ':'), default=str)
        f.close()
        print("get channel Member successfully")

    def dump_to_json(self, download_pic_flag):
        with self.client:
            self.client.loop.run_until_complete(self.get_group_member(download_pic_flag))
