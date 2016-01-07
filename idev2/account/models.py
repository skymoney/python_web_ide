#-*- coding:utf-8 -*-

from django.db import models

class Account(models.Model):
    id = models.AutoField(primary_key=True)