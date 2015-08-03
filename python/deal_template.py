# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_1_0(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        
        sql=("SELECT * FROM `member_userinfo` WHERE userid=%d" % userid)
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)


        senddic={
            'type':'1_1',
            'reply':1
        }
        self.sendmessage(senddic)
        return 1
