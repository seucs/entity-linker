#coding=utf8
import re
import MySQLdb
from MySQLdb import cursors
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from numpy import *   
from sklearn.datasets import load_iris     # import datasets  
  
# load the dataset: iris  
samples = [[1,2],[2,4]]
#print samples   
target = [0,1]   

# import the LogisticRegression  
from sklearn.linear_model import LogisticRegression   
  
classifier = LogisticRegression()  # 使用类，参数全是默认的  

classifier.fit(samples, target)  # 训练数据来学习，不需要返回值  
print target
x = classifier.predict([5, 3])  # 测试数据，分类返回标记  
print classifier.predict_proba([5, 3])    
print x

