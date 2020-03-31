
# 2019-12-16
# created by YHM
# save group message
class groupEnitity(object):
    def __init__(self):
        super().__init__()
        self.group_id = ""
        self.group_account = ""
        self.group_name = ""
        self.group_type = ""
        self.group_description = ""
        self.group_url = ""

        self.group_avatar_url = ""
        self.group_avatar_base64 = ""
        self.group_avatar_store_directory_root = ""
        self.group_avatar_local_filename = ""

        self.group_member_count = 0
        self.group_create_time = None

        self.members = []

    def initWithGroup(self, group):
        self.group_id = group.id
        # 提取username
        if group.username is not None:
            self.group_account = group.username
            url = "https://t.me/" + group.username
            self.group_url = url
        if group.title is not None:
            self.group_name = group.title
        self.group_type = "telegram"
        self.group_create_time = group.date.isoformat(timespec='microseconds')

    def set_Avatar(self, path, filename):
        self.group_avatar_store_directory_root = path
        temp = filename.split('\\')
        self.group_avatar_local_filename = temp[-1]
        self.group_avatar_url = filename

    def set_Member_Account(self,account):
        self.group_member_count = account

    def add_Member(self,mem,flag=False):
        if flag :
            self.members = []
        self.members.append(mem)