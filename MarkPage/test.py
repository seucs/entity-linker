#coding=utf8
import json
import sys
from function.table import tableManager, Table
reload(sys)
sys.setdefaultencoding('utf8')
tables = tableManager().getTable()

with open('data.json','r') as f:
	data_tables = json.loads(f.read())

for nn in xrange(len(data_tables)):
	for ii in xrange(len(data_tables[nn])):
		for jj in xrange(len(data_tables[nn][ii])):
			for c in data_tables[nn][ii][jj]:
				c['candidate'] = c['Mention']
				c['score'] = c['Score']
				c.pop('Mention')
				c.pop('Score')
			data_tables[nn][ii][jj] = {'candidates':data_tables[nn][ii][jj], 'mention':tables[nn][ii][jj]}
	data_tables[nn] = {'data':data_tables[nn], 'nrow':tables[nn].row_num, 'ncol':tables[nn].col_num}


with open('aaa.json','w') as f:
	f.write(json.dumps(data_tables, ensure_ascii=False))