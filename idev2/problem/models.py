#-*- coding:utf-8 -*-

from django.db import models


class Problem(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=100)
    description = models.TextField()

    input_description = models.TextField()
    output_description = models.TextField()

    test_case_code = models.CharField(max_length=100) #测试用例标示，定位测试文件位置

    hints = models.TextField()  #题目提示，json格式

    sample_input = models.CharField(max_length=1000)
    sample_output = models.CharField(max_length=1000)

    tags = models.CharField(max_length=100)

    memory_limit = models.IntegerField() #KB为单位
    time_limit = models.IntegerField() #ms为单位

    contest_id = models.IntegerField(default=-1)    #如果有contest，所属contest的id

    created_time = models.DateTimeField()
    last_update = models.DateTimeField()

    visiable = models.BooleanField(default=True) #是否可见，不可见即删除

    class Meta:
        db_table = 'problem'