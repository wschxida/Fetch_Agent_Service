import json

# 2019-12-16
# created by YHM
# save message
class messageEnitity(json.JSONEncoder):
    def __init__(self):
        super().__init__()
        self.id = ""
        self.author_account = ""
        self.author_name = ""
        self.media_type_code = False
        self.article_title = "M"

        self.article_url = ""
        self.domain_code = ""
        self.article_pubtime_str = ""
        self.article_pubtime = ""
