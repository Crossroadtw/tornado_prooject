import hashlib


class BaseMongoModel(object):

    def __init__(self, mongo_db, mongo_model: str):
        # mongo游标
        self.mongo_cursor = mongo_db[mongo_model]
        # mongo——set字符串
        self.mongo_set_str = mongo_model

    async def insert_table_set(self, mongo_data: dict):
        """
        插入新数据
        :param mongo_data: 要插入的数据
        :return:
        """
        data_and_flag = await self.get_model_data(mongo_data)
        if not data_and_flag:
            return
        if data_and_flag.get('password'):
            p = hashlib.md5()
            p.update(data_and_flag['password'].encode())
            data_and_flag['password'] = p.hexdigest()
        result = await self.mongo_cursor.insert_one(data_and_flag)
        return result

    async def mongo_ensure_index(self, mongo_data: str) -> None:
        """
        创建索引
        :param mongo_data: 要插入集合的数据
        :return: None
        """
        list_indexes = self.mongo_cursor.list_indexes()
        index_list = [_ async for _ in list_indexes]
        if index_list: return
        index_list = await self.model_init_index(mongo_data)
        if index_list:
            index_data = [(_, -1) for _ in index_list]
            await self.mongo_cursor.create_index(index_data)
        index_un_list = await self.model_init_un_index(mongo_data)
        for index_un in index_un_list:
            await self.mongo_cursor.create_index(index_un, unique=True)

    async def get_model_data(self, mongo_data: dict) -> dict:
        """
        验证数据是否符合定义的mongo模型
        :param mongo_data: 要插入集合的数据
        :return: 验证结果
        """
        res = {}
        mongo_model_data = await self.model_init_data(self.mongo_set_str)
        for key, value in mongo_model_data.items():
            if mongo_data.get(key):
                res[key] = mongo_data.get(key)
            elif not mongo_data.get(key) and value.get('default') is not None:
                res[key] = value.get('default')
            elif not mongo_data.get(key) and value.get('default') is None:
                raise Exception(f'{key}为必传参数')
            else:
                raise Exception(f'{key}没有定义')
        return res

    @staticmethod
    async def model_init_data(mongo_key: str) -> dict:
        """
        :param mongo_key: mongo集合名字
        :return: 定义的mongo模型
        """
        return getattr(__import__('model_conf.mongo_model.mongo_model_init', fromlist=['']), f'{mongo_key}_model', {})

    @staticmethod
    async def model_init_index(mongo_key: str) -> list:
        """
        :param mongo_key: mongo集合名字
        :return: 定义的mongo模型
        """
        return getattr(__import__('model_conf.mongo_model.mongo_model_init', fromlist=['']), f'{mongo_key}_index', [])

    @staticmethod
    async def model_init_un_index(mongo_key: str) -> list:
        """
        :param mongo_key: mongo集合名字
        :return: 定义的mongo模型
        """
        return getattr(__import__('model_conf.mongo_model.mongo_model_init', fromlist=['']), f'{mongo_key}_un_index', [])
