#coding=utf8
import tornado.ioloop
from tornado.options import define,options
from handler.ResultHandler import ResultHandler
import cPickle as pickle
import sys, json, os
import platform
reload(sys)
sys.setdefaultencoding('utf8')
        

define('port',default=9000,help='run on the port',type=int)

class Application(tornado.web.Application): 
    def __init__(self):
        handlers = [ 
            (r'/result', ResultHandler)
        ]
        settings = dict( 
             #cookie_secret="7CA71A57B571B5AEAC5E64C6042415DE", 
             static_path = os.path.join(os.path.dirname(__file__).decode('gbk'), u'static'),
             debug=True 
        ) 

        tornado.web.Application.__init__(self, handlers, **settings)

        self.baidu_resArrs = self.dataLoad('../result/wiki')

        print 'result page is OK'


    def dataLoad(self, path):
        with open(path+'/dataTables.data', 'r') as f:
            dataTables = pickle.load(f)


        # 仅含有mention的table
        tables = []
        for dataTable in dataTables:
            table = []
            for i in xrange(dataTable.row):
                table.append([])
                for j in xrange(dataTable.col):
                    table[i].append(dataTable[i][j].name)
            tables.append(table)

        with open(path+'/human_mark.data', 'r') as f:
            human_marks = json.load(f)

        with open(path+'/auto_mark.data', 'r') as f:
            auto_marks = json.load(f)

        # auto_mark和human_mark的dict
        resArrs = []
        right = sum = 0.0
        MRR = 0.0
        for n, table in enumerate(tables):
            res = []
            for i in xrange(len(table)):
                for j in xrange(len(table[i])):
                    mention = table[i][j]
                    human = human_marks[n][i][j]
                    autos = auto_marks[n][i][j]

                    if human == [] or autos == [] or autos == [None]:
                        mark_res = 'None'
                        res.append({'mention':mention, 'human':'None', 'auto':'None', 'res': 'None'})
                        continue

                    auto = autos[0]
                    if human['id'] == auto['id']:
                        right += 1
                        mark_res = 'accept'
                    else:
                        mark_res = 'wrong answer'
                    sum += 1

                    for ii, candidate in enumerate(autos):
                        if human['id'] == candidate['id']:
                            MRR += 1.0 / (ii+1)
                        
                    res.append({'mention':mention,
                                'human':'%s(id:%s)'%(human['name'], human['id']),
                                'auto':'%s(id:%s)'%(auto['name'], auto['id']),
                                'res':mark_res})
            resArrs.append(res)

        print 'precision: %f, MRR: %f'%(right / sum, MRR / sum)
        return resArrs


if __name__ == '__main__':
    tornado.options.parse_command_line() 
    if platform.architecture()[1] == 'WindowsPE':
        Application().listen(options.port, address='127.0.0.1') 
    else:
        Application().listen(options.port, address='121.42.203.161') 
    tornado.ioloop.IOLoop.instance().start()