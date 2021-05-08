import os
import yaml
from utils import dict_to_object

# 项目路径
BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'application')
# 获取静态配置参数
SETTING_DICT = yaml.safe_load(open(os.path.join(os.path.dirname(BASE_PATH), 'config', 'conf.yaml')))

# 添加动态配置参数
SETTING_DYNAMIC = {
    # JWT加密key
    'JWT_KEY': os.urandom(24),
    # 文章md文件位置
    'ARTICLE_FILE': os.path.join(os.path.dirname(BASE_PATH), 'static/article_file')
}

# 更新配置参数
SETTING_DICT.update(SETTING_DYNAMIC)
SETTING = dict_to_object(SETTING_DICT)
