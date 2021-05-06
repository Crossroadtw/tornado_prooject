import time
import datetime

from utils import dict_to_object

# 定义mongo模型
# 用户
tornado_user_db_model = {
    "username": {"type": str},
    "password": {"type": str},
    "super_user": {"type": bool, 'default': False},
    'created': {"type": str, 'default': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
}
tornado_user_db_un_index = ['created']

# 文章
tornado_article_db_model = {
    "filename": {"type": str},
    "file_body": {"type": str},
    "file_show": {"type": bool, 'default': True},
    "file_lable": {"type": list, 'default': list()},
    "file_creat": {"type": str, 'default': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    'created': {"type": str, 'default': int(time.time())}
}
tornado_article_db_un_index = ['filename']
tornado_article_db_index = ['file_lable', 'created']

# 留言板
tornado_messages_db_model = {
    'msg_platform': {"type": str},
    'msg_name': {"type": str},
    'msg_time': {"type": str, 'default': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    'msg_pre_id': {"type": str, 'default': 'all'},
    'msg_body': {"type": str},
    'created': {"type": str, 'default': int(time.time())}
}
tornado_messages_db_index = ['created']


# 注册集合
class MongoDBTableKey(object):
    tornado_user_db = 'tornado_user_db'
    tornado_article_db = 'tornado_article_db'
    tornado_messages_db = 'tornado_messages_db'
