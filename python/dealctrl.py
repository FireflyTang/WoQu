# -*- coding: utf-8 -*
#!/usr/bin/python

import time

#初始化父函数
class dealctrl:
    def __init__(self,con):
        self.recvdic=con.recvdic
        self.address=con.address
        #self.connection=con.connection
        self.db=con.db_cursor
        self.log=con.threadlog

        self.sendmessage=con.sendmessage
        self.getmessage=con.getmessage
        self.sendfile=con.sendfile
        self.getfile=con.getfile

        self.now=int(time.time())
        
