#-*- coding:utf-8 -*-

from client import get_client

def exec_code(code, account, problem_id):
	"""
	执行代码
	"""
	#根据account获取对应虚机id
	contaienr_id = "c58b64789c79"

	#根据problem id 获取case 路径，运行资源限制
	case_path = ""

	#虚机执行
	#一个用户拥有一个虚机，所以暂不需要考虑队列问题
	cmd = "/bin/ls"

	lrun_cmd = "lrun --uid 1 --gid 1 " + cmd + " 3>&1"

	client = get_client()
	exec_info = client.exec_create(contaienr_id, cmd)

	exec_response = client.exec_start(exec_info['Id'])

	print exec_response