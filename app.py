import tornado
import tornado.locks
import tornado.ioloop
import tornado.options
from application import create_app
from config import SETTING


async def main():
    tornado.options.parse_command_line()
    app = await create_app()
    app.listen(SETTING.PORT, SETTING.HOST)
    shut_down = tornado.locks.Event()
    await shut_down.wait()

if __name__ == '__main__':
    tornado.ioloop.IOLoop.current().run_sync(main)
