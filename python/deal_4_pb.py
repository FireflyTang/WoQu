# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_4_pb(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        aid=int(self.recvdic['aid'])

        sql=("INSERT INTO `member_pb`(`pb_userid`, `pb_aid`, `pb_dateline`) VALUES (%d,%d,%d) ON DUPLICATE KEY UPDATE pb_dateline=%d" % (userid,aid,self.now,self.now))
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)

        senddic={
            'type':'4_pb_r',
            'reply':1
        }
        self.sendmessage(senddic)
        return 1
