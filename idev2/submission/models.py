#-*- coding:utf-8 -*-

from django.db import models


class Submission(models.Model):
    id = models.AutoField(primary_key=True)

    account = models.ForeignKey('account.Account', db_column='account')

    submit_time = models.DateTimeField()

    judge_start = models.TimeField(null=True)
    judge_end = models.TimeField(null=True)

    status = models.CharField(max_length=10, default='running') #running accepted fail

    language = models.IntegerField(default=1) #语言默认python 1

    code_path = models.CharField(max_length=100) #代码保存路径

    contest_id = models.IntegerField(null=True) #contest id
    problem_id = models.IntegerField() #problem id

    info = models.TextField(null=True) #存储lrun运行信息

    accepted_info = models.TextField(null=True) #通过后其他信息,得分，case等

    class Meta:
        db_table = 'submission'