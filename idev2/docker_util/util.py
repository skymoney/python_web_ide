#-*- coding:utf-8 -*-

import os

from docker.client import Client
from docker.utils import kwargs_from_env

from idev2.settings import DOCKER_CERT_PATH, DOCKER_HOST, DOCKER_TLS_VERIFY

#pre setting env
os.environ['DOCKER_HOST'] = DOCKER_HOST
os.environ['DOCKER_CERT_PATH'] = DOCKER_CERT_PATH
os.environ['DOCKER_TLS_VERIFY'] = DOCKER_TLS_VERIFY


def get_client():
    kw = kwargs_from_env()
    kw['version'] = '1.20'
    kw['tls'].assert_hostname = False
    client = Client(**kw)

    return client


def create_machine(**kwargs):
    """
    创建一个虚机, 账号激活的时候创建
    :param kwargs:
    :return:
    """
    pass
