#coding=utf8
import time, sys, Queue
import MySQLdb
from MySQLdb import cursors
from multiprocessing.managers import BaseManager
from multiprocessing.sharedctypes import RawArray
from multiprocessing import Process, freeze_support, Array
reload(sys)
sys.setdefaultencoding('utf8')


def work(server_addr):
    # 数据库连接
    from database.db import baidu_db

    # 网络连接
    class QueueManager(BaseManager):
        pass
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')
    print('Connect to server %s...' % server_addr)
    m = QueueManager(address=(server_addr, 5000), authkey='abc')
    m.connect()
    task = m.get_task_queue()
    result = m.get_result_queue()

    
    while True:
        try:
            (nn, ii, jj, name) = task.get(timeout=100)
            candidates = baidu_db.getCandidates(name)
            result.put((nn, ii, jj, candidates))
        except Queue.Empty:
            print 'queue is empty'
            continue
    print 'worker exit.'


if __name__ == '__main__':
    freeze_support()
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
    else:
        num = 3
    print 'total process number is %d'%num

    processes = []
    for i in xrange(num):
        processes.append(Process(target=work, args = ('192.168.1.104',)))

    for p in processes:
        p.start()
    for p in processes:
        p.join()