from abc import ABC

import markdown
from bson import ObjectId

from application.base_handler import BaseHandler
from application.response_model import BaseResponse
from config import SETTING
from model_conf.mongo_model.mongo_cur import BaseMongoModel
from model_conf.mongo_model.mongo_model_init import MongoDBTableKey


class ArticlePage(BaseHandler, ABC):

    async def get(self):
        page = int(self.get_query_argument('page', '1'))
        article_data = self.application.db[MongoDBTableKey.tornado_article_db].find().skip(SETTING.PAGE*(page-1)).limit(SETTING.PAGE)
        article_list = [_ async for _ in article_data]
        await self.render("blog/article_list.html", current_user=self.current_user, articles=article_list)

    async def post(self):
        if not self.current_user: return self.redirect("/")
        file_info = self.request.files.get('article_file', [{}])
        file_name = file_info[0].get('filename')
        file_body = file_info[0].get('body')
        if not file_body:
            return self.write(BaseResponse.FILE_BODY_ERROR)
        file_html = markdown.markdown(file_body.decode(), extensions={'markdown.extensions.fenced_code',
                                                                      'markdown.extensions.tables'})
        mongo_db = BaseMongoModel(self.application.db, MongoDBTableKey.tornado_article_db)
        await mongo_db.insert_table_set({'filename': file_name[:-3], 'file_body': file_html})
        await mongo_db.mongo_ensure_index(MongoDBTableKey.tornado_article_db)
        self.redirect("/article/")


class ArticleInfo(BaseHandler, ABC):

    async def get(self):
        article_id = self.get_query_argument('id')
        article = await self.application.db[MongoDBTableKey.tornado_article_db].find_one({"_id": ObjectId(article_id)})
        await self.render("blog/article_detail.html", current_user=self.current_user, article=article)


class ArticleDelete(BaseHandler, ABC):

    async def get(self):
        if not self.current_user: return self.redirect("/")
        article_id = self.get_query_argument('id')
        await self.application.db[MongoDBTableKey.tornado_article_db].delete_one({"_id": ObjectId(article_id)})
        self.redirect("/article/")
