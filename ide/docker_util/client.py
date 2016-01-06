#-*- coding:utf-8 -*-

import os

from docker.client import Client
from docker.utils import kwargs_from_env

#from conf import DOCKER_HOST, DOCKER_CERT_PATH, DOCKER_TLS_VERIFY
DOCKER_HOST = 'tcp://192.168.99.100:2376'
DOCKER_TLS_VERIFY = "1"
DOCKER_CERT_PATH = '/Users/cheng/.docker/machine/machines/default/'

os.environ['DOCKER_HOST'] = DOCKER_HOST
os.environ['DOCKER_CERT_PATH'] = DOCKER_CERT_PATH
os.environ['DOCKER_TLS_VERIFY'] = DOCKER_TLS_VERIFY

def get_client():
	kw = kwargs_from_env()
	kw['tls'].assert_hostname = False
	kw['version'] = "1.20"

	client = Client(**kw)

	return client