#coding=utf8
import random, multiprocessing, time
from multiprocessing.managers import BaseManager
import cPickle as pickle
from multiprocessing import freeze_support
from database.table import Table, tableManager
from tableStruct import Entity, Mention, DataTable


class QueueManager(BaseManager):
    pass
task_queue = multiprocessing.Queue()
result_queue = multiprocessing.Queue()
def get_task_queue():
    return task_queue
def get_result_queue():
    return result_queue
QueueManager.register('get_task_queue', callable=get_task_queue)
QueueManager.register('get_result_queue', callable=get_result_queue)
manager = QueueManager(address=('192.168.1.104', 5000), authkey='abc')


def communicate(table_num = 0):
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    tm = tableManager('../data/disambiguation_table.xls')
    tables = tm.getTable()
    dataTables = []


    # 任务数量
    count = 0
    if table_num == 0:
        table_num = len(tables)

    for n in xrange(table_num):
        table = tables[n]
        mat = []
        for i in xrange(table.row_num):
            mat.append([])
            for j in xrange(table.col_num):
                name = table[i][j]
                context = table.getMentionContext(i, j)
                task.put((n, i, j, name))
                mat[i].append(Mention(name, context, None))
                count += 1
        dataTables.append(DataTable(table.row_num, table.col_num, mat))
    print 'Put %d tasks' %count


    # 从result队列读取结果:
    print('Try get results...')
    flag = True
    for i in xrange(count):
        (nn, ii, jj, candidates) = result.get(timeout=1000)
        if flag:
            start = time.clock()
            flag = False
        print 'now complete %d, sum is %d'%(i+1,count)
        dataTables[nn][ii][jj].setCandidates(candidates)
    end = time.clock()
    print "%f s"%(end-start)


    with open('dataTables.data','wb') as f:
        pickle.dump(dataTables, f)
    # 关闭
    manager.shutdown()


if __name__ == '__main__':
    freeze_support()
    manager.start()
    communicate()