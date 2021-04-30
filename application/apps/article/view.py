from abc import ABC

from application.base_handler import BaseHandler


class ArticlePage(BaseHandler, ABC):

    async def get(self):
        pass


class ArticleInfo(BaseHandler, ABC):

    async def get(self):
        pass
