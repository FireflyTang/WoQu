# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_4_sc(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        aid=int(self.recvdic['aid'])

        sql=("INSERT INTO `member_sc`(`sc_userid`, `sc_aid`, `sc_dateline`) VALUES (%d,%d,%d) ON DUPLICATE KEY UPDATE sc_dateline=%d " % (userid,aid,self.now,self.now))
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)

        senddic={
            'type':'4_sc_r',
            'reply':1
        }
        self.sendmessage(senddic)
        return 1
