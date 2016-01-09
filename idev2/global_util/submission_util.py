#-*- coding:utf-8 -*-


def submission_auth_check(f):
    """
    检查提交记录是否属于某个账号
    :param f:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        return f(request, *args, **kwargs)
    return wrapper