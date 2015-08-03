# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_1_2(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
                
        userid=int(self.recvdic['userid'])
        username=self.recvdic['username']
        gender=int(self.recvdic['gender'])
        department=int(self.recvdic['department'])
        year=int(self.recvdic['year'])
        edutype=int(self.recvdic['edutype'])
        mobile=int(self.recvdic['mobile'])
        mail=self.recvdic['mail']
        mode=int(self.recvdic['mode'])
        
        if(mode):
            sql=("INSERT INTO `member_userinfo`(`userid`, `username`, `gender`, `department`, `year`, `edutype`,`mobile`,`mail`,`registertime`,`umodifytime`) VALUES (%d,'%s',%d,%d,%d,%d,%d,'%s',%d,%d) ON DUPLICATE KEY UPDATE registertime=%d,umodifytime=%d"%(userid,username,gender,department,year,edutype,mobile,mail,self.now,self.now,self.now,self.now))
        else:
            sql=("UPDATE `member_userinfo` SET `username`='%s',`gender`=%d,`department`=%d,`year`=%d,`edutype`=%d,`mobile`=%d,`mail`='%s',`umodifytime`=%d WHERE userid=%d LIMIT 1" % (username,gender,department,year,edutype,mobile,mail,self.now,userid))
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)
                        
        senddic={
            'type':'1_3',
            'reply':1
        }
        self.sendmessage(senddic)
        return 1
