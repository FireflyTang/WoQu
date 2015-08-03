#-*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *
#from fun_db import *


#验证身份,完成

#self.recvdic=con.recvdic
#self.address=con.address
#self.connection=con.connection
#self.con=con
#seld.db_cursor=con.db_cursor

class deal_2_getfile(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        self.con.sendfile('test2.jpeg')
        
