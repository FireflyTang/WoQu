# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_4_dz(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        aid=int(self.recvdic['aid'])
        
        sql=("SELECT * FROM `activity_dz` WHERE dz_userid=%d AND dz_aid=%d LIMIT 1" % (userid,aid))
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)
        db_re_rowcount=self.db.rowcount
        if(not(db_re_rowcount)):
            sql=("UPDATE `activity_list` SET dz=dz+1,amodifytime=%d WHERE aid=%d LIMIT 1" % (self.now,aid))
            self.log.write("sql: %s\n" % sql)
            self.db.execute(sql)

            sql=("INSERT INTO `activity_dz`(`dz_userid`, `dz_aid`, `dz_dateline`) VALUES (%d,%d,%d)" % (userid,aid,self.now))
            self.log.write("sql: %s\n" % sql)
            self.db.execute(sql)
        
        senddic={
            'type':'4_dz_r',
            'reply':1
        }
        self.sendmessage(senddic)
        return 1
