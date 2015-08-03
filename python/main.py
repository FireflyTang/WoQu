# -*- coding: utf-8 -*
#!/usr/bin/python

import socket
from fun_db import db_cursor_list_init
import multiprocessing

from con import con

import traceback

import time
from fun_dealerr import dealerr 

port=4321
maxconnect=4
mainlog=open('./log/mainlog.log','a',1)
db_cursor_list=db_cursor_list_init(maxconnect,mainlog)
mutex_errlog = multiprocessing.Lock()
connectioncount=0

def conthread(connection,address):
    global db_cursor_list
    starttime=time.time()
    mypid=int(multiprocessing.current_process().name)-1
    
    #可以选择每个线程记录一个日志，也可选择公用一个日志
    #threadlog=open(('./log/processlog/%d.log' % mypid),'a',1)
    threadlog=open('./log/processlog/1.log','a',1)
    #线程号
    now=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    threadlog.write(('nowtime : %s\n' % now))
    threadlog.write("new process begins\n")
    mainlog.write("time: %s \n%d : start\n" % (now,mypid))

    #连接信息
    threadlog.write("connection info : %s\n" % connection)

    #地址信息
    threadlog.write("remote address info : %s %s\n" % (address))
    
    #根据当前的连接个数获取下一个连接的游标
    db_cursor=db_cursor_list[mypid]
    threadlog.write("db_cursor info : %s\n" % db_cursor)
    
    threadlog.write("process runs\n")

    #一个连接类
    newcon=con(connection,address,db_cursor,threadlog)
    
    try:
        #执行连接类->选择处理类->执行处理类
        newcon.run()
        #捕获任何错误,先显示后记录
    except Exception as conerr:
        threadlog.write("!!!!!!!!!!!!!!!!!!!!!CONNECTION ERROR: %s, %s \n" % (Exception,conerr))
        info = traceback.format_exc()
        threadlog.write(("%s" % info ))
        
        with mutex_errlog:
           dealerr(id,'connection error',info)
        
        #只有连接错误才返回-1，进程错误不返回
        senddic={
            'type':'0_0',
            'err':'-1'
            }
        newcon.sendmessage(senddic)
        threadlog.write("disconnected with err\n")
    finally:
        
        #time.sleep(5)
        #newcon.close()#断开连接，调用连接控制父类,由客户端断开

        endtime=time.time()
        threadlog.write("time used %f\n" % (endtime-starttime))
        threadlog.write("connection finished\n--------------------------\n")

        mainlog.write("%d : end\n" % mypid)
        threadlog.flush()
        threadlog.close()
        del newcon#析构
        

def process_init():
    multiprocessing.current_process().name=multiprocessing.current_process().name[-1]


pool=multiprocessing.Pool(maxconnect,process_init)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1) 
mainlog.write("------------------------------------\ntry to bind port : %d\n" % port)
sock.bind(('115.28.225.144', port))
mainlog.write("all db_cursors: %s \n" % db_cursor_list)

#开始监听
sock.listen(maxconnect*10)
mainlog.write("listening %d connections\n" % maxconnect)
mainlog.write("server is ready\n")

#开始等数据
mainlog.write("wait for connection\n")

while True:
    connection,address = sock.accept()
    mainlog.write("--------------------\nconnection count= %d "% connectioncount)
    connectioncount+=1
    pool.apply_async(conthread,(connection,address))
        



