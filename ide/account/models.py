#-*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine

from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Account(Base):
	__tablename__ = 'account'

	id = Column(Integer, primary_key=True)
	email = Column(String(50))
	name = Column(String(50))
	passwd = Column(String(50))



class RuntimeMachine(Base):
	"""
	账号关联虚机配置
	memory，cpu，文件挂载目录，
	"""
	__tablename__ = 'runtime_machine'

	id = Column(Integer, primary_key=True)

	account = Column(Integer, ForeignKey('account.id'))

	container_id = Column(String(50)) #container id after creating container

	mem_limit = Column(Integer) #限制内存，MB为单位
	cpu_limit = Column(Integer) #占用百分比

	volume_dir = Column(String(200)) #共享文件挂载目录

	last_modify = Column(DateTime) #最近修改时间