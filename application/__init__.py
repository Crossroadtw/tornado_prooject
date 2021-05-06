import os
import tornado.web
import tornado.options
from concurrent.futures import ThreadPoolExecutor

from config import SETTING, BASE_PATH
from model_conf.mongo_model import mongo_db
from model_conf.redis_cur import redis_db

# 多线程
class Executor(ThreadPoolExecutor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        # 单例
        if not getattr(cls, '_instance', None):
            cls._instance = ThreadPoolExecutor(max_workers=10)
        return cls._instance


class Application(tornado.web.Application):

    def __init__(self, db, redis_cur):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.db = db
        self.redis_db = redis_cur
        urls = self.get_urls()
        # print('urls', urls)
        for url in urls:
            print('http://{}:{}'.format(SETTING.HOST, SETTING.PORT) + url[0])
        settings = dict(
            template_path=self.get_templates_path(),
            static_path=self.get_static_path(),
            debug=SETTING.DEBUG,
            cookie_secret="chione"
        )
        super().__init__(urls, **settings)

    def get_urls(self):
        """
        获取各个app的url
        :return:
        """
        app_path = os.path.join(self.base_path, 'apps')
        app_urls = []
        for filename in os.listdir('./application/apps'):
            temp_path = os.path.join(app_path, filename)
            if os.path.isdir(temp_path) and "__pycache__" not in temp_path:
                model_name = 'application.apps.' + filename + '.__init__'
                url = getattr(__import__(model_name, fromlist=['']), 'tornado_url')
                app_urls.extend(url)
        return app_urls

    @staticmethod
    def get_templates_path():
        return os.path.join(os.path.dirname(BASE_PATH), 'templates')

    @staticmethod
    def get_static_path():
        return os.path.join(os.path.dirname(BASE_PATH), 'static')


async def create_app() -> Application:
    """创建app"""
    mongo_cursor = mongo_db
    redis_cursor = redis_db
    application = Application(mongo_cursor, redis_cursor)
    return application
