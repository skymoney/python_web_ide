# -*- coding:utf-8 -*-

import os
from idev2.settings import BASE_DIR, CODE_ROOT_PATH, CASE_ROOT_PATH, \
    DOCKER_CODE_PATH, DOCKER_CASE_PATH

ROOT_IMG = 'ubuntu:lrun_env'  # 默认的基准image
CREATE_CMD = '/bin/bash'

MEMORY_LIMIT = '512m'  # 默认限制内存为512mb
MEMORY_LIMIT_VALUE = 512 #数据库记录

CPU_LIMIT_VALUE = 1024
