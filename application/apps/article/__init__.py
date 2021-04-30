import os

# 获取当前app名
from application.apps.article.view import ArticleInfo, ArticlePage

url_base_name = os.path.dirname(__file__).split("/")[-1]

# 定义url
tornado_url = [
    # 文章列表
    (rf"/{url_base_name}/", ArticlePage),
    # 文章展示/删除
    (rf"/{url_base_name}/[^/]*", ArticleInfo)
]
