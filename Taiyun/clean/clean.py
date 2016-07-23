#coding=utf8
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
from urllib import unquote


#decode
def urlcode(filenames):
	for name in filenames:
		with open(name,'r') as f:
			s = unquote(f.read().decode('unicode-escape').encode('utf-8'))
		with open(name,'w') as f:
			f.write(s)

def clean(filenames):

	a = re.compile(u'<http://[^>]+?resource/')
	b = re.compile(u'> <.+?> ')

	for name in filenames:
		with open(name,'r') as f:
			s = f.read()
			s = re.sub(a,'',s)
			s = re.sub(b,'\t',s)
			s = s.replace('> .','')

		with open(name,'w') as f:
			f.write(s)


filenames = ['../data/2.0_zhwiki_disambiguations_zh.nt', '../data/3.0_baidubaike_disambiguations_zh.nt', '../data/3.0_hudongbaike_disambiguations_zh.nt']
urlcode(filenames)
clean(filenames)