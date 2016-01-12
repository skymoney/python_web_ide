#-*- coding:utf-8 -*-

from django.db import models


class Contest(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    description = models.TextField()

    problem_nums = models.IntegerField()     #比赛包含的题目数，用于随机出题

    start = models.DateTimeField()
    end = models.DateTimeField()

    random = models.BooleanField(default=False) #是否是随机比赛，如果是随机比赛，需要报名时分配题目

    create_time = models.DateTimeField()

    class Meta:
        db_table = 'contest'


class ContestJoin(models.Model):
    """
    比赛参加信息
    """
    id = models.AutoField(primary_key=True)

    contest_id = models.IntegerField()
    account_id = models.IntegerField()

    join_time = models.DateTimeField()

    class Meta:
        db_table = 'contest_join'


class ContestRandomProblems(models.Model):
    #如果比赛是随机比赛，记录这里的
    id = models.AutoField(primary_key=True)

    contest_id = models.IntegerField()
    account_id = models.IntegerField()

    problem = models.ForeignKey('problem.Problem', db_column='problem')

    class Meta:
        db_table = 'contest_random_problems'
