#coding=utf8
import sys
import json
import re
import MySQLdb
from MySQLdb import cursors
reload(sys)
sys.setdefaultencoding('utf8')



# 生成Title数据表
def setTitle():
    label_path = '1.0_clean_baidu_labels_zh.nt'
    no_zhPattern = re.compile(u'[^\u4e00-\u9fa5]+')

    count = 0
    for s in open(label_path,'r'):
        s = s.decode('utf8')
        if re.sub(no_zhPattern,'',s) == '':
            continue
        title = TitleCache(title=s)
        db.add(title)
        count+=1
        if count % 10000 == 0:
            db.commit()
            print count
    db.commit()

# 生成Redirect数据表
def setRedirect():
    redirect_path = '1.0_clean_baidu_redirects_zh.nt'

    red_map = {}
    count = 0
    for s in open(redirect_path,'r'):
        s = s.decode('utf8')
        try:
            (par,redir) = s.split('\t',2)
            redir = redir.replace('\n','')
        except:
            continue
        
        par_t = db.query(TitleCache).filter(TitleCache.title == par).first()
        redir_t = db.query(TitleCache).filter(TitleCache.title == redir).first()
        if par_t == None or redir_t == None:
            continue
        red_map[par_t.id] = redir_t.id
        count+=1
        if count % 10000 == 0:
            print count

    count = 0
    for par,redir in red_map.iteritems():
        db.add(RedirectCache(parent=par, redirect = redir))
        count+=1
        if count % 10000 == 0:
            db.commit()
            print count
    db.commit()

# 生成Property数据表
def setProperty():
    property_path = '1.0_clean_baidu_property_zh.nt'
    no_zhPattern = re.compile(u'[^\u4e00-\u9fa5]+')
    count=0
    pro_map = {}
    #for s in open(property_path,'r'):
    #    s = s.decode('utf8')
    #    (title,proper, s) = s.split('\t',3)

    #    _title = db.query(TitleCache).filter(TitleCache.title == title).first()
    #    if _title == None:
    #        continue
    #    _id = _title.id
    #    count+=1
    #    if count % 10000 == 0:
    #        print count
    #    try:
    #        pro_map[_id][proper]=1
    #    except:
    #        pro_map[_id] = {}
    #        pro_map[_id][proper]=1

    #with open('aaa.json','w') as f:
    #    f.write(json.dumps(pro_map, ensure_ascii=False))

    pro_map = json.loads(open('aaa.json','r').read())

    count=0
    for id, proper in pro_map.iteritems():
        for p in proper.keys():
            if re.sub(no_zhPattern,'',p) == '':
                continue
            db.add(PropertyCache(title_id=id, property=p))
            count+=1
            if count % 100000 == 0:
                db.commit()
                print count
    db.commit()

# 生成倒排索引
def preprocess():
    titleArr = db.query(TitleCache).all()
    for t in titleArr:
        title = t.title
        id = t.id
        print title,id
