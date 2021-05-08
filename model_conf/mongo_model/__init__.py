# mongo
from motor.motor_asyncio import AsyncIOMotorClient

from config import SETTING

# 连接mongo
MONGO_CONNECTION = AsyncIOMotorClient(
    SETTING.MONGO_HOST,
    SETTING.MONGO_POORT
)

# 选择mongo数据库
mongo_db = MONGO_CONNECTION[SETTING.MONGO_DATABASE]
