#coding=utf8
from handler.BaseHandler import BaseHandler

class ResultHandler(BaseHandler):



    def get(self):
        id = int(self.get_argument('id'))
        _sum = _right = 0

        _resArr = self.baidu_resArrs[id]
        for res in _resArr:
            if res['res'] == 'accept':
                _sum += 1
                _right += 1
            elif res['res'] == 'wrong answer':
                _sum += 1

        self.render("../html/result.html",id=id, sum=_sum, right=_right, resArr = _resArr)
