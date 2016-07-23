#coding=utf8
import cPickle as pickle
from tableStruct import *
from operator import itemgetter 
import sys, json
reload(sys)
sys.setdefaultencoding('utf8')

classifier = None
def train(train_dataTables, human_marks):
    global classifier
    samples =[]
    target = []

    for nn, dataTable in enumerate(train_dataTables):
        for i in xrange(dataTable.row):
            for j in xrange(dataTable.col):
                mention = dataTable[i][j]
                if mention.cid == -1:
                    continue
                eids = dataTable.get_eids(i, j)
                words = dataTable.get_words(i, j)
                entites = dataTable.get_entities(i ,j)
                true_id = human_marks[nn][i][j]['id']
                for ii, entity in enumerate(mention.candidates):
                    prior = entity.popular
                    SR = mention.getSR(ii, entites)
                    res = int(true_id == entity.id)
                    samples.append([prior, SR])
                    target.append(res)

    from sklearn import svm   
    classifier = svm.SVC(probability=True)
    classifier.fit(samples, target)

def predict(vec):
    return classifier.predict_proba(vec)[0][1]
     

# return has_changed
def ICA(dataTable):
    has_changed = False
    priRes = [None] * dataTable.row
    for i in xrange(dataTable.row):
        priRes[i] = [None] * dataTable.col
    for i in xrange(dataTable.row):
        for j in xrange(dataTable.col):
            priRes[i][j] = [None] * len(dataTable[i][j].candidates)

    for i in xrange(dataTable.row):
        for j in xrange(dataTable.col):
            mention = dataTable[i][j]
            if mention.cid == -1:
                continue
            eids = dataTable.get_eids(i, j)
            words = dataTable.get_words(i, j)
            entites = dataTable.get_entities(i ,j)
            i_max = (-1,-1)
            for ii, entity in enumerate(mention.candidates):
                prior = entity.popular
                SR = mention.getSR(ii, entites)
                res = predict([[prior, SR]])
                priRes[i][j][ii] = {'name':entity.title, 'id':entity.id, 'p':-res}

                if res > i_max[1]:
                    i_max = (ii, res)
            if mention.cid != i_max[0]:
                mention.cid = i_max[0]
                has_changed = True

    if has_changed:      
        return has_changed, None

    for i in xrange(dataTable.row):
        for j in xrange(dataTable.col):
            priRes[i][j] = sorted(priRes[i][j], key=itemgetter('p'))
    return has_changed, priRes



            
def main(kb):
    with open('../result/%s/dataTables.data'%kb,'r') as f:
        dataTables = pickle.load(f)
    with open('../result/%s/human_mark.data'%kb,'r') as f:
        human_marks = json.load(f)
    

    train(dataTables[:20],human_marks[:20])

    auto_marks = []
    max_iter = 100
    for i, dataTable in enumerate(dataTables):    
        for n in xrange(max_iter):
            has_changed, res = ICA(dataTable)
            if not has_changed:
                auto_marks.append(res)
                break
        print u'第%d张表,迭代%d次'%(i,n)

    with open('../result/%s/LIEGE/auto_mark.data'%kb,'w') as f:
        json.dump(auto_marks, f, ensure_ascii=False)

main('wiki')