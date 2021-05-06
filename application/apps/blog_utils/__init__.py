import os

url_base_name = os.path.dirname(__file__).split("/")[-1]

# 定义url
tornado_url = [
    # 留言板
    # (rf"/{url_base_name}[/]?", Message)
]
