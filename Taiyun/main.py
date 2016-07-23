#coding=utf8
import MachineLearning
import cPickle as pickle
import json
from tableStruct import Mention, DataTable

def main():
	with open('../result/hudong/dataTables.data','r') as f:
		dataTables = pickle.load(f)

	auto_marks = []
	for nn, dataTable in enumerate(dataTables):
		mentions = []
		for i in xrange(dataTable.row):
			for j in xrange(dataTable.col):
				mentions.append(dataTable[i][j])
		auto_mark = MachineLearning.main(mentions, dataTable.row, dataTable.col)
		auto_marks.append(auto_mark)
		#print auto_marks
		print u'第%d个表格标注完成'%nn

	with open('../result/hudong/taiyun/auto_mark.data','w') as f:
		json.dump(auto_marks, f)
	#-------------------------------------------------------------------------------

	with open('../result/baidu/dataTables.data','r') as f:
		dataTables = pickle.load(f)

	auto_marks = []
	for nn, dataTable in enumerate(dataTables):
		mentions = []
		for i in xrange(dataTable.row):
			for j in xrange(dataTable.col):
				mentions.append(dataTable[i][j])
		auto_mark = MachineLearning.main(mentions, dataTable.row, dataTable.col)
		auto_marks.append(auto_mark)
		print u'第%d个表格标注完成'%nn

	with open('../result/baidu/taiyun/auto_mark.data','w') as f:
		json.dump(auto_marks, f)

	#-------------------------------------------------------------------------------

	with open('../result/wiki/dataTables.data','r') as f:
		dataTables = pickle.load(f)

	auto_marks = []
	for nn, dataTable in enumerate(dataTables):
		mentions = []
		for i in xrange(dataTable.row):
			for j in xrange(dataTable.col):
				mentions.append(dataTable[i][j])
		auto_mark = MachineLearning.main(mentions, dataTable.row, dataTable.col)
		auto_marks.append(auto_mark)
		print u'第%d个表格标注完成'%nn

	with open('../result/wiki/taiyun/auto_mark.data','w') as f:
		json.dump(auto_marks, f)


main()