# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_1_5(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        
        userid=int(self.recvdic['userid'])
        personalsign=self.recvdic['personalsign']
        if(personalsign):
            sql=("UPDATE `member_userinfo` SET `personalsign`='%s',`umodifytime`=%d WHERE userid=%d LIMIT 1" % (personalsign,self.now,userid))
            self.log.write("sql: %s\n" % sql)
            self.db.execute(sql)
        
        senddic={
            'type':'1_5_r',
            'reply':1
        }
        self.sendmessage(senddic)
        return 1
