import os
import yaml
from utils import dict_to_object

SETTING_DYNAMIC = {
    'JWT_KEY': os.urandom(24)
}
BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'application')
SETTING_DICT = yaml.safe_load(open(os.path.join(os.path.dirname(BASE_PATH), 'config', 'conf.yaml')))
SETTING_DICT.update(SETTING_DYNAMIC)
SETTING = dict_to_object(SETTING_DICT)
