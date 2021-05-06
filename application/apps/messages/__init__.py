import os

from application.apps.messages.view import Message, MessageDelete

# 获取当前app名
url_base_name = os.path.dirname(__file__).split("/")[-1]

# 定义url
tornado_url = [
    # 留言板
    (rf"/{url_base_name}[/]?", Message),
    # 删除
    (rf"/{url_base_name}/delete[/]?", MessageDelete)
]
