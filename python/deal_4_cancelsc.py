# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_4_cancelsc(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        aid=int(self.recvdic['aid'])

        sql=("DELETE FROM `member_sc` WHERE sc_userid=%d AND sc_aid=%d LIMIT 1" % (userid,aid))
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)

        senddic={
            'type':'4_cancelsc_r',
            'reply':1
        }
        self.sendmessage(senddic)
        return 1
