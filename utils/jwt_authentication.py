import jwt, datetime

from config import SETTING


def authorization(token) -> str:
    """
    :param token: token
    :return: 用户名
    """
    ver_token = verify_jwt_token(token)
    if ver_token:
        return ver_token['data']['username']
    return ''


def verify_jwt_token(token) -> dict:
    """
    解密token返回dict
    :param token: token
    :return: dict
    """
    # noinspection PyBroadException
    try:
        data = jwt.decode(token, SETTING.JWT_KEY, algorithms=SETTING.JWT_FLAG)
    except:
        return {}
    return data


def generate_token(user_name) -> str:
    """
    生成token
    :param user_name: 用户名
    :return: token(str)
    """
    token = jwt.encode({
        'exp': datetime.datetime.now() + datetime.timedelta(days=30),  # 过期时间
        'iat': datetime.datetime.now(),  # 开始时间
        'data': {
            'username': user_name
        }}, SETTING.JWT_KEY, algorithm=SETTING.JWT_FLAG)

    return token
