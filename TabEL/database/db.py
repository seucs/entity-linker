#coding=utf8
import MySQLdb
import json
import os
import Levenshtein
import cPickle as pickle
from MySQLdb import cursors
from tableStruct import Entity

class database:
    def __init__(self, db_name):
        if db_name == 'wiki':
            kb_name = 'wiki_kb'
        elif db_name == 'baidu':
            kb_name = 'kb'
        elif db_name == 'hudong':
            kb_name = 'hudong_kb'

        self.db = MySQLdb.connect(host='192.168.1.104',user="root",passwd="",db=kb_name ,charset="utf8", cursorclass=cursors.SSCursor)  
        self.cur = self.db.cursor()
        self.db_titles = []
        self.db_disambiguations = []

        print 'db is loading......'
        if os.path.exists('title_disambiguation.data'):
            with open('title_disambiguation.data','r') as f:
                self.db_titles, self.db_disambiguations = pickle.load(f)
        else:
            self.load_save_db()
        print 'db has been loaded !'

    def load_save_db(self):
        # 全部title信息 用于遍历     
        self.cur.execute("select * from title")
        for row in self.cur:
            self.db_titles.append(row)

        # 全部disambiguation信息 用于遍历
        self.cur.execute("select * from disambiguation")
        for row in self.cur:
            self.db_disambiguations.append(row)
        
        save = (self.db_titles, self.db_disambiguations)
        with open('title_disambiguation.data','wb') as f:
            pickle.dump(save, f)

    def getCandidates(self, mention, threshold=0.7):
        res = []

        # 遍历title表
        for id, title, link_count in self.db_titles:
            m_score = Levenshtein.ratio(title, mention)
            if m_score > threshold:
                self.cur.execute("select abstract from abstract where id = %s"%id)
                context = self.cur.fetchall()
                if context != ():
                    context = json.loads(context[0][0])

                RE = []
                self.cur.execute("select to_id from link where from_id = %s"%id)
                linkto_ids = self.cur.fetchall()
                if linkto_ids != ():
                    for to_id in linkto_ids:
                        RE.append(to_id[0])

                res.append(Entity(title, id, m_score, context, link_count, RE))

        # 遍历disambiguation表
        for id, title, dis_context, link_count in self.db_disambiguations:
            m_score = Levenshtein.ratio(title, mention)
            if m_score > threshold:
                title += '[%s]'%dis_context
                self.cur.execute("select abstract from abstract where id = %s"%id)
                context = self.cur.fetchall()
                if context != ():
                    context = json.loads(context[0][0])
                    context.append(dis_context)

                RE = []
                self.cur.execute("select to_id from link where from_id = %s"%id)
                linkto_ids = self.cur.fetchall()
                if linkto_ids != ():
                    for to_id in linkto_ids:
                        RE.append(to_id[0])

                res.append(Entity(title, id, m_score, context, link_count, RE))
        return res

    

    


baidu_db = database('hudong')