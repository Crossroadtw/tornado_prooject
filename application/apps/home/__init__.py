import os

from tornado.web import RedirectHandler

from application.apps.home.view import MainHandler, Login, Logout, Closed

# 获取当前app名
url_base_name = os.path.dirname(__file__).split("/")[-1]

# 定义url
tornado_url = [
    # 主页面重定向
    (r'[/]?', RedirectHandler, {'url': 'home'}),
    # 登录接口
    (rf"/login[/]?", Login),
    # 退出登录
    (rf"/logout[/]?", Logout),
    # 404
    (rf"/closed[/]?", Closed),
    # 主页面
    (rf"/{url_base_name}[/]?", MainHandler)
]
