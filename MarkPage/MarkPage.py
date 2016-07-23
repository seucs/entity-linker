#coding=utf8
import tornado.ioloop
from tornado.options import define,options
from sqlalchemy.orm import scoped_session, sessionmaker
from handler.MainHandler import MainHandler, HomeHandler, RemarkHandler
from handler.ResultHandler import ResultHandler
from database.db import engine
from tableStruct import *
import cPickle as pickle
import sys
import json
import os
import platform
reload(sys)
sys.setdefaultencoding('utf8')
        

define('port',default=8000,help='run on the port',type=int)

class Application(tornado.web.Application): 
    def __init__(self):
        handlers = [ 
            (r'/mark', MainHandler),
            (r'/', HomeHandler),
            (r'/remark', RemarkHandler)
            #(r'/result', ResultHandler)
        ]
        settings = dict( 
             #cookie_secret="7CA71A57B571B5AEAC5E64C6042415DE", 
             static_path = os.path.join(os.path.dirname(__file__).decode('gbk'), u'static'),
             debug=True 
        ) 


        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine))

        with open('dataTables.data','r') as f:
            dataTables = pickle.load(f)

        self.tables = []
        for dataTable in dataTables:
            data = []
            for i in xrange(dataTable.row):
                data.append([])
                for j in xrange(dataTable.col):
                    mention = dataTable[i][j].name
                    candidates = []
                    real_candidates = dataTable[i][j].candidates
                    for entity in real_candidates:
                        e_data = {}
                        e_data['score'] = entity.score
                        e_data['name'] = entity.title
                        e_data['id'] = entity.id
                        candidates.append(e_data)
                    data[i].append({'mention':mention, 'candidates':candidates})
            table = {'ncol':dataTable.col, 'nrow':dataTable.row, 'data':data}
            self.tables.append(table)
        print 'mark page is OK'
        #with open('auto_mark.json','r') as f:
        #    self.auto_mark_tables = json.load(f)
        #with open('human_mark.json','r') as f:
        #    self.human_mark_tables = json.load(f)



if __name__ == '__main__':
    tornado.options.parse_command_line() 
    if platform.architecture()[1] == 'WindowsPE':
        Application().listen(options.port, address='192.168.1.104') 
    else:
        Application().listen(options.port, address='121.42.203.161') 
    tornado.ioloop.IOLoop.instance().start()