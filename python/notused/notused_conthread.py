# -*- coding: utf-8 -*
#!/usr/bin/python

from con import con
import _thread
import traceback
import threading



#一个类是一个线程
class conthread:
    mutex = threading.Lock()
    def __init__(self,conargs):
        #线程号
        self.threadid=_thread.get_ident()
        print(self.threadid,":","new thread begins")

        #连接信息
        self.connection=conargs['connection']
        print(self.threadid,":","connection info :" , self.connection)

        #地址信息
        self.address=conargs['address']
        print(self.threadid,":","remote address info :" , self.address)

        #根据当前的连接个数获取下一个连接的游标
        self.db_cursor_list=conargs['db_cursor_list']
        self.db_cursor=self.db_cursor_list[self.db_cursor_list[0]+1]
        print(self.threadid,":","db_cursor info:",self.db_cursor)

        mutex.acquire()
        self.db_cursor_list[0]+=1
        mutex.release()
        
        #运行线程
        self.run()
        
    def run(self):

        print(self.threadid,":","thread runs")

        #一个连接类
        newcon=con(self.connection,self.address,self.db_cursor)

        try:
            newcon.run()#执行连接类->选择处理类->执行处理类

        #捕获任何错误
        except Exception as conerr:
            print("!!!!!!!!!!!!!!!!!!!!!ERROR:",Exception,":",conerr)
            info = traceback.format_exc()
            print(info)
            ##发邮件

        finally:
            
            mutex.acquire()
            self.db_cursor_list[0]-=1
            mutex.release()
            
            newcon.close()#断开连接，调用连接控制父类
            print(self.threadid,":","disconnected")
            del newcon#析构

#线程池的错误收集回调函数
def handle_exception(request,exc_info):
    if not isinstance(exc_info,tuple):
        print(request)
        print(exc_info)
        raise SystemExit
    print ("**** Exception occured in request #%s: %s" % (request.requestID,exc_info))
