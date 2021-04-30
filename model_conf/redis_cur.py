import redis
from config import SETTING

pool = redis.ConnectionPool(host=SETTING.REDIS_HOST, port=SETTING.REDIS_PORT)
redis_db = redis.Redis(connection_pool=pool)


class RedisDB(redis_db):

    def __init__(self) -> None:
        super().__init__()
