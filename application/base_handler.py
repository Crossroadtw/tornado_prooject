from abc import ABCMeta
from tornado.web import RequestHandler

from application import Executor
from utils.jwt_authentication import authorization


class BaseHandler(RequestHandler, metaclass=ABCMeta):
    executor = Executor()

    def initialize(self):
        """
        设置头之后，get之前，一些初始化操作
        :return:
        """
        self.set_default_headers()

    async def prepare(self):
        """
        init之后get之前，相当于请求钩子、中间件的
        :return:
        """
        author = authorization(self.get_secure_cookie('X-Auth-Token'))
        if author:
            self.current_user = author

    def on_finish(self):
        """
        get之后，相当于请求钩子、中间件的
        :return:
        """

    def set_default_headers(self) -> None:
        """
        所有与方法之前
        :return:
        """
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名也可以是*
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    async def get_mongo_find_one(self, mongoo_set: str, sql_info: dict) -> dict:
        """查一条数据"""
        data_info = await self.application.db[mongoo_set].find_one(sql_info)
        return data_info

