#coding=utf8
import cPickle as pickle
import json, sys, re, math
import Levenshtein
import MySQLdb
import cPickle as pickle
from MySQLdb import cursors
from urllib import unquote
from tableStruct import *
reload(sys)
sys.setdefaultencoding('utf8')

baidu_db = MySQLdb.connect(host='192.168.1.103',user="root",passwd="",db='kb' ,charset="utf8", cursorclass=cursors.SSCursor)  
baidu_cur = baidu_db.cursor()
hudong_db = MySQLdb.connect(host='192.168.1.103',user="root",passwd="",db='hudong_kb' ,charset="utf8", cursorclass=cursors.SSCursor)  
hudong_cur = hudong_db.cursor()
wiki_db = MySQLdb.connect(host='192.168.1.103',user="root",passwd="",db='wiki_kb' ,charset="utf8", cursorclass=cursors.SSCursor)  
wiki_cur = wiki_db.cursor()

def findId_hudong(hs):
    hid = None
    if hs.find('[') != -1:
        hsl = re.sub(r'\[.*\]', '', hs)
        hudong_cur.execute("select id, context from disambiguation where title = '%s'"%hsl)
        for row in hudong_cur:
            if hs == '%s[%s]'%(hsl, row[1]):
                hid = row[0]
    else:
        hudong_cur.execute("select id from title where title = '%s'"%hs)
        for row in hudong_cur:
            hid = row[0]
    return hid

def findId_wiki(ws):
    wid = None
    wiki_cur.execute("select id from title where title = '%s'"%ws)
    for row in wiki_cur:
        wid = row[0]
    return wid

def findId_baidu(bs):
    bid = None
    if bs.find('[') != -1:
        bsl = re.sub(r'\[.*\]', '', bs)
        baidu_cur.execute("select id, context from disambiguation where title = '%s'"%bsl)
        for row in baidu_cur:
            if bs == '%s[%s]'%(bsl, row[1]):
                bid = row[0]
    else:
        baidu_cur.execute("select id from title where title = '%s'"%bs)
        for row in baidu_cur:
            bid = row[0]
    return bid

def setSameAs():
    count = 0
    for s in open('sameAs/bw.nt'):

        s = s.decode('utf8')
        bs, ws = s.split()
        if bs.find("'") != -1 or ws.find("'") != -1:
            continue
        bid = findId_baidu(bs)
        wid = findId_wiki(ws)
        if bid != None and wid != None:
            baidu_cur.execute("insert into bw_sameAs(baidu_id, wiki_id) values (%d, %d)"%(bid, wid))

        count += 1
        if count % 10000 == 0:
            print count
    baidu_db.commit()

def getCategoryDict(db_name):
    res = {}
    for ii in xrange(1,4):
        with open('type/%s%d.txt'%(db_name, ii), 'r') as f:
            for line in f:
                line = line.decode('utf8')
                try:
                    category, title = line.split()
                except:
                    continue
                if not res.has_key(title):
                    res[title] = [category]
                else:
                    res[title].append(category)
    return res

def setCategory(db_name):
    db_dict={'baidu':'kb', 'hudong':'hudong_kb', 'wiki':'wiki_kb'}
    db = MySQLdb.connect(host='192.168.1.103',user="root",passwd="",db=db_dict[db_name] ,charset="utf8", cursorclass=cursors.SSCursor)  
    cur = db.cursor()

    def findTable_Id(title):
        table = id = None
        if title.find("'") != -1:
            return table, id
        if title.find('[') != -1:
            title_l = re.sub(r'\[.*\]', '', title)
            cur.execute("select id, context from disambiguation where title = '%s'"%title_l)
            for row in cur:
                if title == '%s[%s]'%(title_l, row[1]):
                    id, table = row[0], u'disambiguation'       
        else:
            cur.execute("select id from title where title = '%s'"%title)
            for row in cur:
                id, table = row[0], u'title'
        return table, id

    dict = getCategoryDict(db_name)
    for title,category in dict.iteritems():
        category = json.dumps(category, ensure_ascii=False)
        table, id = findTable_Id(title)
        if id != None:
            cur.execute("update %s set category='%s' where id=%d"%(table, category, id))
    db.commit()
    
def getId(kb, title):
    if kb=='baidu':
        return findId_baidu(title)
    if kb=='hudong':
        return findId_hudong(title)
    if kb=='wiki':
        return findId_wiki(title)

def saveTrain(filepath):
    res = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.decode('utf8')
            try:
                kb1, title1, kb2, title2 = line.split()
                id1, id2 = getId(kb1, title1), getId(kb2, title2)
                if id1 == None or id2 == None:
                    continue
                res.append([kb1, id1, kb2, id2])
            except:
                continue
    with open(filepath, 'w') as f:
        json.dump(res, f, ensure_ascii=False)

def setTrain():
    content = {'bh':{'sample':[], 'target':[]},
                'bw':{'sample':[], 'target':[]},
                'hw':{'sample':[], 'target':[]}
                }

    with open('train/negative.json', 'r') as f:
        s = json.load(f)
        for i, item in enumerate(s):
            kb1, id1, kb2, id2 = item
            if kb1 == 'baidu' and kb2 == 'hudong':
                content['bh']['sample'].append([id1, id2])
                content['bh']['target'].append(0)
            elif kb1 == 'baidu' and kb2 == 'wiki':
                content['bw']['sample'].append([id1, id2])
                content['bw']['target'].append(0)
            elif kb1 == 'hudong' and kb2 == 'wiki':
                content['hw']['sample'].append([id1, id2])
                content['hw']['target'].append(0)

    with open('train/positive.json', 'r') as f:
        s = json.load(f)
        for i, item in enumerate(s):
            kb1, id1, kb2, id2 = item
            if kb1 == 'baidu' and kb2 == 'hudong':
                content['bh']['sample'].append([id1, id2])
                content['bh']['target'].append(1)
            elif kb1 == 'baidu' and kb2 == 'wiki':
                content['bw']['sample'].append([id1, id2])
                content['bw']['target'].append(1)
            elif kb1 == 'hudong' and kb2 == 'wiki':
                content['hw']['sample'].append([id1, id2])
                content['hw']['target'].append(1)

    with open('train/trainId.json', 'w') as f:
        json.dump(content, f, ensure_ascii=False)

def getMsgbyId(kb, id):
    if kb == 'baidu':
        m_db, m_cur = baidu_db, baidu_cur
    elif kb == 'hudong':
        m_db, m_cur = hudong_db, hudong_cur
    elif kb == 'wiki':
        m_db, m_cur = wiki_db, wiki_cur

    category = title = None
    context = []
    
    m_cur.execute("select title, category from title where id = %d"%id)
    for row in m_cur:
        title, category = row

    ### 从title中获取数据
    if title != None:
        if category != None:
            category = json.loads(category)
        else:
            category = []
        m_cur.execute("select abstract from abstract where id = %d"%id)
        for row in m_cur:
            context = json.loads(row[0])
        return title, context, category

    ### 从disambiguation中获取数据
    m_cur.execute("select title, context, category from disambiguation where id = %d"%id)
    for row in m_cur:
        title, context, category = row
    if category != None:
        category = json.loads(category)
    else:
        category = []
    m_cur.execute("select abstract from abstract where id = %d"%id)
    a_context = []
    for row in m_cur:
        a_context = json.loads(row[0])
    a_context.append(context)
    context = a_context

    return title, context, category

def cosine(vec1, vec2):
    if len(vec1) * len(vec2) == 0:
        return 0.0
    union = set(vec1) & set(vec2)
    return len(union) / (math.sqrt(len(vec1)) * math.sqrt(len(vec2)))

def sameCategory(category1, category2):
    union = set(category1) & set(category2)
    return float(len(union) > 0)

def getVec(kb, id1, id2):
    if kb == 'bh':
        title1, context1, category1 = getMsgbyId('baidu', id1)
        title2, context2, category2 = getMsgbyId('hudong', id2)
    if kb == 'bw':
        title1, context1, category1 = getMsgbyId('baidu', id1)
        title2, context2, category2 = getMsgbyId('wiki', id2)
    if kb == 'hw':
        title1, context1, category1 = getMsgbyId('hudong', id1)
        title2, context2, category2 = getMsgbyId('wiki', id2)

    title_r = Levenshtein.ratio(title1, title2)
    context_r = cosine(context1, context2)
    category_r = sameCategory(category1, category2)

    return (title_r, context_r, category_r, 0.0)

def setCandidatesVec():
    with open('../result/baidu/dataTables.data') as f:
        baidu_dataTables = pickle.load(f)
    with open('../result/hudong/dataTables.data') as f:
        hudong_dataTables = pickle.load(f)
    with open('../result/wiki/dataTables.data') as f:
        wiki_dataTables = pickle.load(f)

    table_num = len(baidu_dataTables)

    res = []
    for n in xrange(table_num):
        row = baidu_dataTables[n].row
        col = baidu_dataTables[n].col
        res.append([[None]*col]*row)
        for i in xrange(row):
            for j in xrange(col):
                baidu_candidates = baidu_dataTables[n][i][j].candidates
                hudong_candidates = hudong_dataTables[n][i][j].candidates
                wiki_candidates = wiki_dataTables[n][i][j].candidates
                b_num = len(baidu_candidates)
                h_num = len(hudong_candidates)
                w_num = len(wiki_candidates)

                dict = {'bh':[[None]*h_num]*b_num, 'bw':[[None]*w_num]*b_num, 'hw':[[None]*w_num]*h_num}
                for ii in xrange(b_num):
                    for jj in xrange(h_num):
                        dict['bh'][ii][jj] = getVec('bh', baidu_candidates[ii].id, hudong_candidates[jj].id)
                for ii in xrange(b_num):
                    for jj in xrange(w_num):
                        dict['bw'][ii][jj] = getVec('bw', baidu_candidates[ii].id, wiki_candidates[jj].id)
                for ii in xrange(h_num):
                    for jj in xrange(w_num):
                        dict['hw'][ii][jj] = getVec('hw', hudong_candidates[ii].id, wiki_candidates[jj].id)
                res[n][i][j] = dict

    with open('train/dataVecs.json', 'w') as f:
        json.dump(res, f, ensure_ascii=False)



