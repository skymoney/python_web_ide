#-*- coding:utf-8 -*-

import os
from .util import get_client

from account.models import RuntimeMachine
from problem.models import Problem
from code_util.util import switch_case_path, switch_code_path

from idev2.settings import CASE_ROOT_PATH

def exec_code(submission):
    """
    判题核心处理
    根据account_id 获取对应虚机
    根据problem_id 获取case路径和运行资源限制
    submission_id 用于更新运行状态和结果信息
    :param submission
    """
    runtime_machine = RuntimeMachine.objects.get(account=submission.account)

    machine_id = runtime_machine.container_id

    client = get_client()

    #代码路径需要映射，从宿主机目录到虚机目录
    target_code_path = switch_code_path(submission.code_path)
    #case文件需要根据problem中的case code生成
    problem = Problem.objects.get(id=submission.problem_id)
    if problem.test_case_code:
        origin_case_path = os.path.join(CASE_ROOT_PATH,
            problem.test_case_code, ".py").replace("\\", "/")
    else:
        origin_case_path = ""

    case_file_path = switch_case_path(origin_case_path)
    cmd_str = "python " + case_file_path + " " + target_code_path
    cmd_str = "sleep 3"
    lrun_cmd = "lrun --uid 1 --gid 1 " + cmd_str

    exec_info = client.exec_create(container=machine_id, cmd=lrun_cmd)

    exec_result = client.exec_start(exec_info['Id'])

    #执行结束，更新submission状态
    submission.info = exec_result


    return 0