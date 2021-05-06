class BaseResponse(object):
    """返回数据"""
    SUCCESS_DATA = lambda data: {'status': 0, 'msg': '请求成功', 'data': data}
    UNKNOWN_ERROR = {'status': 101, 'msg': '未知错误', 'data': {}}
    PARAM_ERROR = {'status': 102, 'msg': '参数缺失', 'data': {}}
    PARAM_TYPE_ERROR = {'status': 103, 'msg': '参数类型错误', 'data': {}}
    USER_ERROR = {'status': 104, 'msg': '账号或密码错误', 'data': {}}
    FILE_BODY_ERROR = {'status': 105, 'msg': '未获取到文件', 'data': {}}
