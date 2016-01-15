#-*- coding:utf-8 -*-

"""
监控虚机实例
crontab任务，每5分钟运行一次，扫描数据库心跳表，如果是超时，关闭对应虚机
心跳包每隔一分钟更新一次，所以心跳表中记录最新时间间隔大于1分钟则证明失去心跳
防止一些时间误差和用户体验，改成间隔大于3分钟则关闭
"""

from datetime import datetime
import MySQLdb

from docker.client import Client
from docker.utils import kwargs_from_env

###setting
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'
MYSQL_DB = 'py_ide'


class MonitorClient(object):
    def __init__(self):
        kw = kwargs_from_env()
        kw['tls'].assert_hostname = False

        self.client = Client(kw)

    def shutdown(self, container):
        """
        关闭指定id的虚机
        :param container: id或id list
        :return:
        """
        if type(container) == list:
            #id list
            for id in container:
                self.client.stop(container=id)
        else:
            #单个container id
            self.client.stop(container=container)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.client.close()


class DatabaseConnection(object):
    def __init__(self):
        self.connection = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT,
                    user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
        self.cursor = self.connection.cursor()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cursor.close()
        self.connection.close()


def monitor():
    heartbeat_list = []
    with DatabaseConnection() as connection:
        sql = """select runtime_heartbeat.*, runtime_machine.container_id from runtime_heartbeat
              left join runtime_machine on runtime_heartbeat.account_id = runtime_machine.account"""
        resut_data = connection.query(sql)

        for data in resut_data:
            heartbeat_list.append((data[1], data[2], data[3]))

    now_date = datetime.now()
    to_stop_list = []
    for heartbeat in heartbeat_list:
        timedelta = now_date - heartbeat[1]
        if timedelta.seconds > 180:
            #失去心跳，关闭对应的虚机,加到待删除列表中，批量删除
            to_stop_list.append(heartbeat[2])

    with MonitorClient() as client:
        client.shutdown(to_stop_list)

    print 'close all'


if __name__ == '__main__':
    monitor()