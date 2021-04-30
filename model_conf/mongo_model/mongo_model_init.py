import datetime

from utils import dict_to_object

# 定义mongo模型
tornado_user_db_model = {
    "username": {"type": str},
    "password": {"type": str},
    "super_user": {"type": bool, 'default': False},
    'created': {"type": str, 'default': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
}


# 注册集合
class MongoDBTableKey(object):
    tornado_user_db = 'tornado_user_db'
