# coding:utf-8
import sklearn.metrics
import numpy as np
import jieba
#jieba.load_userdict("userdict.txt")
import jieba.posseg as pseg

def getData(Mentions,S,E,contextMention,contextEntity, id):
	for mention in Mentions:
		jieba.add_word(mention.name)
		
		S.append(mention.name)
		id.append('-') #一个占位符，没有实际意义
		contextMention[mention.name] = mention.context
	for item in Mentions:
		temp = []
		cnt = 0
		for candidate in item.candidates:
			if cnt > 100:
				break
			cnt += 1
			temp.append(candidate.title)
			contextEntity[candidate.title] = candidate.context

			id.append(candidate.id)
		E.append(temp)

# element{序号：mention/entity}
# 计算element
def setNumber(S, E, element):
	i = 0
	mentionLen = len(S)
	elementLen = len(element)
	for item in S:
		element[i] = item
		i += 1

	for itemList in E:
		for item in itemList:
			element[i] = item
			i += 1

def jaccard_similarity_score(context1, context2, flag1, flag2):
	#print 'context1', context1
	try:
		if flag1 and len(context1)!=0:
			temp = context1[-1]
			context1.pop()
			context1 += list(pseg.cut(temp))
		if flag2 and len(context1)!=0:
			temp = context2[-1]
			context2.pop()
			context2 += list(pseg.cut(temp))
	except:
		pass

	mySet = set(context1 + context2)
	a1 = []
	a2 = []
	for item in mySet:
		if item in context1:
			a1.append(1)
		else:
			a1.append(0)
		if item in context2:
			a2.append(1)
		else:
			a2.append(0)
	#print sklearn.metrics.jaccard_similarity_score(a1,a2)
	return sklearn.metrics.jaccard_similarity_score(a1,a2)
	
# element[i]和element[j]的contextSim
def contextSim(contextMention,contextEntity,S,element,i,j):
	if element[i]==u'一触即发' and element[j]==u'一触即发[2010年吴彦祖主演电影]':
		iiii = 1

	mentionLen = len(S)
	if i < mentionLen and j >= mentionLen:
		if len(contextMention[element[i]]) * len(contextEntity[element[j]]) == 0:
			return 0
		return jaccard_similarity_score(contextMention[element[i]],contextEntity[element[j]], False, True)
	elif j < mentionLen and i >= mentionLen:
		if len(contextEntity[element[i]]) * len(contextMention[element[j]]) == 0:
			return 0
		return jaccard_similarity_score(contextEntity[element[i]],contextMention[element[j]], True, False)
	elif i >= mentionLen and j >= mentionLen:
		if len(contextEntity[element[i]]) * len(contextEntity[element[j]]) == 0:
			return 0
		return jaccard_similarity_score(contextEntity[element[i]],contextEntity[element[j]], True, True)

# element[i]和element[j]是否在同一个RDF里面
def isRDF(i,j):
	return 0

# 经过一次迭代之后和之前的列向量P的模差值
def increase(P,Plast):
	return np.sqrt(sum((Plast - P) ** 2))


# Mentions是唯一的传入的数据，由朴哥提供
def main(Mentions, nrow, ncol):
	def getStateTransitionMatrix(contextMention,contextEntity,S,element):
		elementLen = len(element)

		# 计算W
		W = np.zeros([elementLen,elementLen],float)	
		mentionLen = len(S)

		# W(mention,mention)
		for i in range(mentionLen):
			for j in range(mentionLen):
				W[i][j] = 0.1
		for i in range(elementLen):
			W[i][i] = 0.01

		# W(mention,entity)
		for k in range(mentionLen):
			score = [] # mention与实体的相似度，由朴哥提供
			title = [] # 实体的名称，由朴哥提供
			for entity in Mentions[k].candidates:
				score.append(entity.score)
				title.append(entity.title)

			cnt = mentionLen
			for j in range(mentionLen,elementLen):
				for i in xrange(0, len(score)):
					if j>=cnt and element[j] == title[i]: 
						W[k][j] = 0.99 * (a1 * score[i] + b1 * contextSim(contextMention,contextEntity,S,element,k,j)) + 0.01
					else:
						W[k][j] = 0.01
				if W[k][j]==0:
					W[k][j] = 0.01

				W[j][k] = W[k][j]
	
		# W(entity,entity)
		for i in range(mentionLen,elementLen):
			for j in range(mentionLen,elementLen):
				if i != j:
					W[i][j] = 0.99 * (a2 * isRDF(i,j) + b2 * contextSim(contextMention,contextEntity,S,element,i,j)) + 0.01
					W[j][i] = W[i][j]

		# 计算A
		A = np.zeros([elementLen,elementLen],float)
		for i in range(elementLen):
			denominator = 0.0
			for k in range(elementLen):
					denominator += W[i][k]
			for j in range(0,elementLen):
				A[i][j] = W[i][j] / denominator

		return A

	# A的方阵，P是行向量
	def disambiguate(A,upLimit):
		# 初始化P
		mentionLen = len(S)
		elementLen = len(element)
		P = np.zeros(elementLen, float)
		
		for i in range(mentionLen):
			P[i] = 1.0 / elementLen
		for i in range(mentionLen,elementLen):
			P[i] = 0

		# 上一次迭代的P
		Plast = P
		oneMat = np.ones([elementLen, elementLen])
		
		d = 0.85

		AA = np.dot((1-d)/elementLen, oneMat) + np.dot(d, A.T)
		for i in xrange(upLimit):
			P = np.dot(AA, Plast)
			if increase(P,Plast) < epsion:
				break
			Plast = P
			#print 'P', P
		return P

	# 获得最后的结果并存在一个list中，list中的每一个是一个实体
	def getResultFromP(S,P,element):
		def isEntityVarious(itemList):
			flag = False
			for item in itemList:
				if '[' in item:
					flag = True
					break
			return flag

		ret = []
		retID = []

		mentionPos = 0
		entityPos = len(S)
		for itemList in E:
			maxPos = entityPos
			tempPos = entityPos # for postFix

			for item in itemList:
				if P[entityPos] > P[maxPos]:
					maxPos = entityPos
				entityPos += 1
			
			if True or not isEntityVarious(itemList):
				for item in itemList:
					if item == element[mentionPos]:
						maxPos = tempPos
						break
					tempPos += 1

			if len(itemList)==0:
				ret.append(None)
				retID.append(None)
			else:   
				ret.append(element[maxPos])
				retID.append(id[maxPos])

			mentionPos += 1

		#print ret

		retTable = []
		for ii in xrange(nrow):
			retTable.append([])
			for jj in xrange(ncol):
				if ret[ii*ncol+jj] == None:
					retTable[ii].append({})
				else:
					retTable[ii].append({'name':ret[ii*ncol+jj], 'id':retID[ii*ncol+jj]})

		#print retTable

		candidateList = []
		entityPos = len(S)
		mentionPos = 0		
		for itemList in E:
			candidateList.append([])
			posList = [] # 按照P对位置做一个排序posList
			for i in xrange(entityPos, entityPos + len(itemList)):
				posList.append([P[i], i])
			sorted(posList)

			try:
				for similarity, jj in posList:
					candidateList[mentionPos].append({'name':element[jj], 'id':id[jj]})
			except:
				print mentionPos

			if len(posList) == 0:
				candidateList[mentionPos].append(None)

			entityPos += len(itemList)
			mentionPos += 1

		candidateLists = []
		for ii in xrange(nrow):
			candidateLists.append([])
			for jj in xrange(ncol):
				if candidateList[ii*ncol+jj] == None:
					candidateLists[ii].append([])
				else:
					candidateLists[ii].append(candidateList[ii*ncol+jj])

		for i in xrange(len(retTable)):
			for j in xrange(len(retTable[i])):
				li = candidateLists[i][j]
				
				for n in xrange(len(li)):
					if retTable[i][j] == li[n]:
						li.insert(0, li[n])
						li.pop(n + 1)
						break
		
		return candidateLists


	S = [] # mention集合
	E = [] # entitys集合

	id = []
	element = {} # mention与entity编号之后的元素 {序号：mention/entity}
	
	a1 = a2 = 0.7
	b1 = b2 = 0.3

	contextMention = {} # 行列除掉自己 mention对应的上下文
	contextEntity = {} # 利用RDF.txt文件 entity对应的上下文

	epsion = 0.000001
	upLimit = 50000 # 迭代上限

	ret = [] # 最终的结果 entity

	# 获得S，E,contextMention，contextEntity
	getData(Mentions,S,E,contextMention,contextEntity, id)
	setNumber(S, E, element)

	A = getStateTransitionMatrix(contextMention,contextEntity,S,element)
	P = disambiguate(A, upLimit)

	return getResultFromP(S,P,element)
