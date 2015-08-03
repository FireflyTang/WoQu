# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *
import time
#from fun_isTsinghua import *

#1_1注册
#self.recvdic=con.recvdic
#self.address=con.address
#self.connection=con.connection
#self.con=con
#seld.db_cursor=con.db_cursor

class deal_1_1(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        
        self.db_cursor.execute('select * from test')
        for r in self.db_cursor:
            print("row_number:"+str(self.db_cursor.rownumber))
            print("a:"+str(r[0])+"b:"+str(r[1]))

        self.senddic={
            'type':'1_2',
            'result':'你'
        }


        self.con.sendmessage(self.senddic)
