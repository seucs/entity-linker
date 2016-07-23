#coding=utf8
import math

class Mention:
    def __init__(self, name, context, candidates):
        self.name = name #string
        self.context = context #list of string(other mentions which in same col or row)
        self.cid = -1 # int candidates id
        if candidates == None:
            return
        self.setCandidates(candidates)
        

    def setCandidates(self, candidates):
        self.candidates = candidates #list of Entity

        # 计算流行度并将最大值的cid找出来
        sum_count = 0.0
        for entity in self.candidates:
            sum_count += entity.link_count
            
        i_max = (-1,-1)
        for i, entity in enumerate(self.candidates):
            if sum_count == 0:
                entity.popular = 0.0 
            else:
                entity.popular = entity.link_count / sum_count

            if sum_count > i_max[1]:
                i_max = (i, sum_count)
        self.cid = i_max[0]

    # 这边可以改成用编辑距离实现,目前完全匹配
    # 这里魔改了一下，之后效果不行再调试
    def getSR(self, ii, entities):
        res = 0.0
        cur_e = self.candidates[ii]
        for e in entities:
            res += self.cosine(cur_e.context, e.context)
        res /= len(entities)
        return res
                        

    def getMES(self, ii, eids, words):
        cur_e = self.candidates[ii]
        MES_E = self.cosine(eids, cur_e.RE)
        MES_W = self.cosine(words, cur_e.context)

        return MES_E, MES_W

    def cosine(self, vec1, vec2):
        if len(vec1) * len(vec2) == 0:
            return 0.0
        union = set(vec1) & set(vec2)
        return len(union) / (math.sqrt(len(vec1)) * math.sqrt(len(vec2)))


class Entity:
    def __init__(self, title, id, score, context, link_count, RE):
        self.title = title #string
        self.id = id #int
        self.score = score  #float
        self.context = context #list of string
        self.link_count = link_count # int
        self.popular = 0.0 # float
        self.RE = RE  # list of entity


class DataTable:
    def __init__(self, row, col, mat):
        self.col = col
        self.row = row
        self.mat = mat

    def __getitem__(self, i):
        return self.mat[i]

    # 获取同行同列所有暂时实体id
    def get_eids(self, r, c):
        res = []
        for i in range(self.row):
            if i == r:
                continue
            cid = self.mat[i][c].cid
            if cid == -1:
                continue
            res.append(self.mat[i][c].candidates[cid].id)

        for j in range(self.col):
            if j == c:
                continue
            cid = self.mat[r][j].cid
            if cid == -1:
                continue
            res.append(self.mat[r][j].candidates[cid].id)
        return res

    # 获取同行同列所有words
    def get_words(self, r, c):
        return self.mat[r][c].context

    # 获得同行同列所有暂时实体
    def get_entities(self, r, c):
        res = []
        for i in range(self.row):
            if i == r:
                continue
            cid = self.mat[i][c].cid
            if cid == -1:
                continue
            res.append(self.mat[i][c].candidates[cid])

        for j in range(self.col):
            if j == c:
                continue
            cid = self.mat[r][j].cid
            if cid == -1:
                continue
            res.append(self.mat[r][j].candidates[cid])
        return res

