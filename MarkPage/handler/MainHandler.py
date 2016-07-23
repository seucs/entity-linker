#coding=utf8
from handler.BaseHandler import BaseHandler
from database.db_cache import ResultCache, StatusCache
import json

class MainHandler(BaseHandler):
    def get(self):
        
        id = self.db.query(StatusCache).first().progress
        if id >= len(self.tables):
            self.write(u'md标完了你还标')
            return

        self.db.query(StatusCache).filter(
            StatusCache.progress == id).update({
            StatusCache.progress : id + 1,
            StatusCache.status : 0
        })
        try:
            self.db.commit()
        except:
            self.db.rollback()

        self.render("../html/webpage.html",
                    table = json.dumps(self.tables[id],ensure_ascii=False),
                    m_table = self.tables[id]['data'],
                    page = id,
                    totalpage=len(self.tables)
                    )
        
        
    def post(self):
        pagenum = self.get_argument('pagenum')
        pageresult = self.get_argument('result')
        _status = self.get_argument('status')
        _time = self.get_argument('time')
        _ratio = self.get_argument('mark_ratio')

        res = ResultCache(table_id = pagenum, result = pageresult, status = _status, time = _time, mark_ratio = _ratio)

        if self.db.query(ResultCache).filter(ResultCache.table_id == pagenum).first() != None:
            self.db.query(ResultCache).filter(ResultCache.table_id == pagenum).delete()
        
        self.db.add(res)
        try:
            self.db.commit()
        except:
            self.db.rollback()


class HomeHandler(BaseHandler):
    def get(self):
        id = self.db.query(StatusCache).first().progress
        resArr = self.db.query(ResultCache).all()[::-1]
        _res = []
        for res in resArr:
            _res.append({
                'id':res.table_id,
                'status':res.status,
                'time':res.time,
                'mark_ratio':res.mark_ratio
                })
            
        self.render("../html/home.html",page =id,totalpage=len(self.tables), resArr = _res)


class RemarkHandler(BaseHandler):
    def get(self):

        id = int(self.get_argument('id'))
        print id, len(self.tables)

        if id >= len(self.tables):
            self.write(u'md标完了你还标')
            return

        self.render("../html/webpage.html",
                    table = json.dumps(self.tables[id],ensure_ascii=False),
                    m_table = self.tables[id]['data'],
                    page = id,
                    totalpage=len(self.tables)
                    )