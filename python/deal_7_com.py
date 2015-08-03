# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_7_com(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        aid=int(self.recvdic['aid'])
        content=self.recvdic['content']
        
        sql=("INSERT INTO `activity_comment` (`aid`,`userid`,`content`,`commenttime`) VALUES (%d,%d,'%s',%d)" % (aid,userid,content,self.now))
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)

        cid=self.db.insert_id()
        senddic={
            'type':'7_com_r',
            'reply':1,
            'cid':cid
        }
        self.sendmessage(senddic)
        return 1
