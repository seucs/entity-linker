#coding=utf-8

from sqlalchemy import Column, VARCHAR, INT, TEXT, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class StatusCache(Base):
	__tablename__ = 'status'
	progress = Column(INT, primary_key=True)
	status = Column(INT)


class ResultCache(Base):
	__tablename__ = 'result'
	table_id = Column(INT, primary_key=True)
	result = Column(TEXT)
	status = Column(VARCHAR(255))
	mark_ratio = Column(VARCHAR(255))
	time = Column(DATETIME)