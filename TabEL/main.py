#coding=utf8
from database.table import tableManager
import Levenshtein
import os

from database.db import baidu_db

#tm = tableManager('../data/disambiguation_table.xls')
#tables = tm.getTable()

#for n, table in enumerate(tables):
#    for i in xrange(table.row_num):
#        for j in xrange(table.col_num):
#            name = table[i][j]
#            try:
#                Levenshtein.ratio(name, u'ss')
#            except:
#                print n,i,j,name