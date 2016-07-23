#coding=utf8
import cPickle as pickle
import json, sys
reload(sys)
sys.setdefaultencoding('utf8')

with open('../result/baidu/auto_mark.data', 'r') as f:
    auto_marks = json.load(f)

print auto_marks[0][2][0]