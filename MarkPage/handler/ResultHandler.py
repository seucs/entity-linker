#coding=utf8
from handler.BaseHandler import BaseHandler

class ResultHandler(BaseHandler):
    @property
    def auto_mark_tables(self):
        return self.application.auto_mark_tables

    @property
    def human_mark_tables(self):
        return self.application.human_mark_tables


    def get(self):
        id = int(self.get_argument('id'))
        _resArr = []
        _sum = _right = 0




        for mention, entity in self.auto_mark_tables[id].iteritems():
            res = {}
            res['mention'] = mention
            res['auto'] = entity
            res['human'] = self.human_mark_tables[id][mention]
            if self.human_mark_tables[id][mention] == entity and entity != None:
                _right += 1
                _sum += 1
                res['res'] = 'accept'
            elif entity != None:
                _sum += 1
                res['res'] = 'wrong answer'
            else:
                res['res'] = 'None'
            _resArr.append(res)

        self.render("../html/result.html",id=id, sum=_sum, right=_right, resArr = _resArr)
