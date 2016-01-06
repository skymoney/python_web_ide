#-*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine

from sqlalchemy.dialects.mysql import TINYINT

from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Problem(Base):
	__tablename__ = 'problem'

	id = Column(Integer, primary_key=True)

	title = Column(String(50))
	description = Column(Text())

	input_description = Column(Text())
	output_description = Column(Text())

	test_case_code = Column(String(100)) #测试用例标示，定位测试文件位置

	hints = Column(Text())

	sample_input = Column(String(1000))
	sample_output = Column(String(10000))

	tags = Column(String(100))

	memory_limit = Column(Integer) #KB为单位
	time_limit = Column(Integer) #ms为单位

	created_time = Column(DateTime)
	last_update = Column(DateTime)

	visiable = Column(TINYINT, default=1) #是否可见，不可见即删除


class Contest(Base):
	__tablename__ = 'contest'

	id = Column(Integer, primary_key=True)
