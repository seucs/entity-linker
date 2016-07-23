主要思想：

见刘太云学长毕业论文



数据结构：

```python
S = [] # mention集合, [   m1        ,    m2        , ...]
E = [] # entitys集合, [[e1, e2, ...], [e1, e2, ...], ...] 注意上下的对齐

id = [] # entity存储在数据库里, 所以每个entity都对应一个id, 主要是为了与人工标注的实体比较
element = {} # mention与entity编号之后的元素 {序号：mention 或者 entity}, 论文中的算法借鉴了马尔科夫链的思想, 需要构建一个矩阵, 所以先给mention, entity编号

a1 = a2 = 0.7 # 某经验系数
b1 = b2 = 0.3 # 某经验系数

contextMention = {} # 表格一行一列除掉本身的所有单元格作为mention对应的上下文, {mention : context}
contextEntity = {} # 利用abstract文件得到entity对应的上下文, {entity : context}

epsion = 0.000001 # 马尔科夫链停止的条件
upLimit = 50000 # 迭代次数上限
```



函数解释：

```python
def getData(Mentions,S,E,contextMention,contextEntity, id)
解释：Mentions是输入数据，S、E、contextMention、contextEntity、id都是从Mentions中分类提取，方面后面的直接调用

def setNumber(S, E, element)
解释：将S、E编号放到element中 

def jaccard_similarity_score(context1, context2, flag1, flag2)
解释：计算上下文context1和上下文context2的jaccard相似度, 
flag1为True: context1为mention的上下文, 
flag1为False: context1为entity的上下文, 
flag2同理

def contextSim(contextMention,contextEntity,S,element,i,j)
解释：计算element[i]和element[j]的上下文相似度

def increase(P,Plast)
解释：马尔科夫链中的P矩阵, 计算出与上一次的变化量, 作为迭代停止的一个判断标准

def getStateTransitionMatrix(contextMention,contextEntity,S,element)
解释：先获得W, 再由W获得A, 具体计算方法见论文

def disambiguate(A,upLimit)
解释：迭代算法的核心部分, 迭代至变化量小于设定的阈值获得达到设定的最大迭代次数

def getResultFromP(S,P,element)
解释：从最终得到的P中得出结果, 方法是对每个的mention的候选实体取最大的那个候选实体

def main(Mentions, nrow, ncol)
解释：一个总的流程, 调用了上面的函数, 对用户来说只需要简单的调用main就可以完成链接的工作，而不需要自己去考虑调用哪些函数
```



使用说明：

直接调用main，并且传入数据（数据包括表格的所有mention，每个mention对应的候选实体等等），表格的行，表格的列就可以了。本算法是每次处理一个表格。
