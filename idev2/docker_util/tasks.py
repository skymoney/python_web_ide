#-*- coding:utf-8 -*-

import os
from celery import task
from datetime import datetime
from time import time

from .util import get_client

from account.models import RuntimeMachine
from problem.models import Problem
from code_util.util import switch_case_path, switch_code_path

from idev2.settings import CASE_ROOT_PATH

@task()
def exec_code(submission):
    """
    根据提交记录执行代码
    :param submission:
    :return:
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

    if not os.path.isfile(origin_case_path):
        origin_case_path = ''

    case_file_path = switch_case_path(origin_case_path)
    cmd_str = "python " + case_file_path + " " + target_code_path
    lrun_cmd = "lrun --uid 1 --gid 1 " + cmd_str  #虚机中root用户，需要指定uid，gid

    exec_info = client.exec_create(container=machine_id, cmd=lrun_cmd)

    submission.judge_start = datetime.now() #TODO 修改格式
    exec_result = client.exec_start(exec_info['Id'])

    #执行结束，更新submission状态
    submission.info = exec_result
    submission.judge_end = datetime.now()
    submission.accepted_info = '' #通过后生成额外的结果信息
    submission.status = 'accepted' #更新状态

    try:
        submission.save()
    except:
        #log 记录 异常处理，需要重新运行提交代码？ TODO
        pass
