#coding=utf8
import platform
import os

DB_HOST = 'localhost'
DB_USER = 'root'
if platform.architecture()[1] == 'WindowsPE':
    DB_PWD = ''
else:
    DB_PWD = '3676677'
DB_NAME = 'markdata'

TIME_OUT = 7

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db_path = 'mysql://%s:%s@%s/%s?charset=utf8' %(DB_USER, DB_PWD, DB_HOST, DB_NAME)

engine = create_engine(db_path, echo=False,
                   pool_size=100, pool_recycle=10)