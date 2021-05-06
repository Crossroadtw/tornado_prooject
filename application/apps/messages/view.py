import hashlib
from abc import ABC

from bson import ObjectId
from user_agents import parse

from application.base_handler import BaseHandler
from config import SETTING
from model_conf.mongo_model.mongo_cur import BaseMongoModel
from model_conf.mongo_model.mongo_model_init import MongoDBTableKey


class Message(BaseHandler, ABC):

    async def get(self):
        page = int(self.get_query_argument('page', '1'))
        messages = self.application.db[MongoDBTableKey.tornado_messages_db].find().skip(SETTING.PAGE*(page-1)).limit(SETTING.PAGE)
        messages_list = [_ async for _ in messages]
        await self.render("messages/message.html", current_user=self.current_user, messages=messages_list)

    async def post(self):
        username = self.get_body_argument('username')
        commit_info = self.get_body_argument('message')
        agent_info = self.request.headers.get('User-Agent')
        if not all([username, commit_info]):
            return self.redirect("/messages/")
        user_agent = str(parse(agent_info))
        mongo_db = BaseMongoModel(self.application.db, MongoDBTableKey.tornado_messages_db)
        await mongo_db.insert_table_set({'msg_platform': user_agent, 'msg_body': commit_info, 'msg_name': username})
        await mongo_db.mongo_ensure_index(MongoDBTableKey.tornado_messages_db)
        self.redirect("/messages/")


class MessageDelete(BaseHandler, ABC):

    async def get(self):
        if not self.current_user: return self.redirect("/")
        article_id = self.get_query_argument('id')
        await self.application.db[MongoDBTableKey.tornado_messages_db].delete_one({"_id": ObjectId(article_id)})
        self.redirect("/messages/")
