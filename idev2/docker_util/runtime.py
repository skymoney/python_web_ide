#-*- coding:utf-8 -*-

import os
from datetime import datetime
from .util import get_client

from account.models import RuntimeMachine, Account
from problem.models import Problem
from code_util.util import switch_case_path, switch_code_path

from idev2.settings import CASE_ROOT_PATH, DOCKER_CODE_PATH, DOCKER_CASE_PATH, CODE_ROOT_PATH

from .docker_conf import MEMORY_LIMIT, MEMORY_LIMIT_VALUE, CPU_LIMIT_VALUE, \
    ROOT_IMG, CREATE_CMD


def create_runtime(account_id):
    """
    创建虚机，挂载账号目录到虚机中的代码路径下，只读权限
    :return:
    """
    client = get_client()

    #创建挂载目录，不同账号的代码目录不同
    volumes = [DOCKER_CODE_PATH, DOCKER_CASE_PATH]
    volume_binds = {'/'.join([CODE_ROOT_PATH, str(account_id)]) + '/':
                        {'bind': DOCKER_CODE_PATH,
                         'mode': 'ro'},
                    CASE_ROOT_PATH + '/':
                        {'bind': DOCKER_CASE_PATH,
                         'mode': 'ro'},
                    }
    try:
        container_info = client.create_container(image=ROOT_IMG, command=CREATE_CMD, tty=True,
            volumes=volumes, host_config=client.create_host_config(binds=volume_binds, mem_limit=MEMORY_LIMIT))

        #记录虚机记录
        runtime_machine = RuntimeMachine(account=Account.objects.get(id=account_id),
                                         container_id=container_info['Id'],
                                         cpu_limit=CPU_LIMIT_VALUE, mem_limit=MEMORY_LIMIT_VALUE,
                                         volume_dir=':'.join(volume_binds.keys()),
                                         last_modify=datetime.now())

        runtime_machine.save()
    except Exception, e:
        #TODO log记录
        pass

    del client


def start_runtime(container_id):
    """
    启动虚机，用在登录时候
    :param container_id:
    :return:
    """
    client = get_client()

    container_info = client.inspect_container(container=container_id)

    if container_info and not container_info['State']['Running']:
        #容器有效且没有运行
        client.start(container=container_id)

    del client

def restart_runtime(container_id, force=False):
    """
    重启容器
    :param container_id:
    :param force: 是否强制重启
    :return:
    """
    client = get_client()

    all_running_container_ids = map(lambda x:x['Id'], client.containers(quiet=True))

    if container_id in all_running_container_ids:
        if force:
            client.stop(container=container_id)
        else:
            del client
            return True

    #不在运行或已经被终止
    try:
        client.start(container=container_id)
        del client
        return True
    except Exception, e:
        del client
        return False

def stop_runtime(container_id):
    client = get_client()

    client.stop(container=container_id)

    del client

def exec_code(submission):
    """
    deprecated
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