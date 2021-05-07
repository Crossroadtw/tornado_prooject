import hashlib
from abc import ABC

from application.base_handler import BaseHandler
from model_conf.mongo_model.mongo_model_init import MongoDBTableKey
from utils.jwt_authentication import generate_token


class MainHandler(BaseHandler, ABC):

    async def get(self):
        await self.render("blog/index.html", current_user=self.current_user)


class Login(BaseHandler, ABC):

    async def post(self):
        username = self.get_body_argument('username')
        password = self.get_body_argument('password')
        if not all([username, password]):
            return self.redirect("/")
        # 密码哈希
        p = hashlib.md5()
        p.update(password.encode())
        sql_info = {
            'username': username,
            'password': p.hexdigest()
        }
        # 查询数据
        user_info = await self.get_mongo_find_one(MongoDBTableKey.tornado_user_db, sql_info)
        if user_info:
            # 设置cookie OR token
            self.set_secure_cookie('X-Auth-Token', generate_token(username))
        self.redirect("/")


class Logout(BaseHandler, ABC):

    async def get(self):
        self.current_user = None
        self.clear_all_cookies()
        self.redirect("/")


class Closed(BaseHandler, ABC):

    async def get(self):
        message = '制作中'
        await self.render("error/404.html", message=message)
