#-*- coding:utf-8 -*-

import os
from datetime import datetime
from idev2.settings import CODE_ROOT_PATH, \
    CASE_ROOT_PATH, DOCKER_CODE_PATH, DOCKER_CASE_PATH


def save_code(account_id, problem_id, code):
    """
    保存代码到文件 ROOT_PATH/<account>/<problem_id>/timestamp.py
    :param code:
    :return:
    """
    target_file = datetime.now().strftime("%Y%m%d%H%M%S") + ".py"
    target_dir = os.path.join(CODE_ROOT_PATH, str(account_id), str(problem_id))

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    target_code_path = os.path.join(target_dir, target_file)

    with open(target_code_path, 'wb') as code_file:
        code_file.write(code)

    return target_code_path


def switch_code_path(path):
    """
    从宿主机路径切换到虚机路径
    :return:
    """
    return path.replace(CODE_ROOT_PATH, DOCKER_CODE_PATH)


def switch_case_path(case_path):
    return case_path.replace(CASE_ROOT_PATH, DOCKER_CASE_PATH)