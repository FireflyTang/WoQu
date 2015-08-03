# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_8_apply(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        aid=int(self.recvdic['aid'])
        
        sql=("SELECT * FROM `activity_apply` WHERE userid=%d AND aid=%d LIMIT 1" % (userid,aid))        
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)
        db_re_rowcount=self.db.rowcount
        if(not(db_re_rowcount)):
            sql=("SELECT `portraitmd5` FROM `member_userinfo` WHERE userid=%d LIMIT 1" % userid )
            self.log.write("sql: %s\n" % sql)
            self.db.execute(sql)
            portraitmd5=self.db.fetchone()['portraitmd5']            

            sql=("INSERT INTO `activity_apply` (`userid`,`portraitmd5`,`aid`,`applytime`) VALUES (%d,'%s',%d,%d) " % (userid,portraitmd5,aid,self.now))
            self.log.write("sql: %s\n" % sql)
            self.db.execute(sql)

            sql=("UPDATE `activity_list` SET peopleapply=peopleapply+1,amodifytime=%d WHERE aid=%d LIMIT 1" % (self.now,aid))
            self.log.write("sql: %s\n" % sql)
            self.db.execute(sql)
            
        senddic={
            'type':'deal_8_apply_r',
            'reply':1
            }
        self.sendmessage(senddic)
        return 1
