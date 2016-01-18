#-*- coding:utf-8 -*-

from django.db import models


class Account(models.Model):
    id = models.AutoField(primary_key=True)

    email = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    passwd = models.CharField(max_length=50)

    active_code = models.CharField(max_length=100)
    is_active = models.IntegerField()

    join_date = models.DateTimeField()
    last_login = models.DateTimeField()

    class Meta:
        db_table = 'account'


class RuntimeMachine(models.Model):
    id = models.AutoField(primary_key=True)

    account = models.ForeignKey('account.Account', db_column='account')

    container_id = models.CharField(max_length=100)

    mem_limit = models.IntegerField()
    cpu_limit = models.IntegerField()
    volume_dir = models.CharField(max_length=500)

    last_modify = models.DateTimeField()

    class Meta:
        db_table = 'runtime_machine'


class RuntimeHeartBeat(models.Model):
    """
    心跳记录
    """
    id = models.AutoField(primary_key=True)

    account_id = models.IntegerField()
    last_beat = models.DateTimeField()

    class Meta:
        db_table = 'runtime_heartbeat'