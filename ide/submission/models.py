#-*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine

from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Submission(Base):
	__tablename__ = 'submission'

	id = Column(Integer, primary_key=True)

	account = Column(Integer, ForeignKey('account.id'))

	problem = Column(Integer, ForeignKey('problem.id'))
	