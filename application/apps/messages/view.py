import datetime
import json
import time
from abc import ABC

import tornado.websocket
from bson import ObjectId
from user_agents import parse

from application.base_handler import BaseHandler
from config import SETTING
from model_conf.mongo_model.mongo_cur import BaseMongoModel
from model_conf.mongo_model.mongo_model_init import MongoDBTableKey
from utils.send_email import sned_email


class Message(BaseHandler, ABC):

    async def get(self):
        page = int(self.get_query_argument('page', '1'))
        messages = self.application.db[MongoDBTableKey.tornado_messages_db].find({
            'msg_pre_id': 'all'
        }).skip(SETTING.PAGE*(page-1)).limit(SETTING.PAGE)
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


class MessageEmail(BaseHandler, ABC):

    def get(self):
        chat_num = self.application.redis_db.get('chat:num')
        messages = self.application.redis_db.zrange('message', 0, -1)
        messages = map(lambda k: json.loads(k), messages)

        self.render('messages/chat.html', chat_num=chat_num, messages=messages)

    def post(self):

        print('有人提醒我上线啦')
        msg = "有人提醒你上线聊天啊"
        try:
            sned_email(msg)
            self.write({'status': 1})
        except:
            self.write({'status': 0})

    def put(self):
        chat_num = self.application.redis_db.get('chat:num')
        self.write({'chat_num': chat_num.decode()})


class MessageChat(tornado.websocket.WebSocketHandler, ABC):
    waiters = set()

    def open(self):
        MessageChat.waiters.add(self)
        self.application.redis_db.incr('chat:num')

    def on_close(self):
        MessageChat.waiters.remove(self)
        self.application.redis_db.decr('chat:num')

    def on_message(self, message):

        message_dict = {'text': message, 'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.application.redis_db.zadd('message', {json.dumps(message_dict): int(time.time())})
        if self.application.redis_db.ttl('message') <= 60:
            self.application.redis_db.expire('message', 300)

        MessageChat.send_updates(message_dict)

    @classmethod
    def send_updates(cls, message_dict):
        print("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(message_dict)
            except:
                print('推送更新失败')
