# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_7_require_com(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        aid=int(self.recvdic['aid'])
        lastcid=int(self.recvdic['lastcid'])
        neednum=int(self.recvdic['neednum'])
        
        sql=("\
SELECT * FROM (SELECT * FROM `activity_comment` WHERE aid=%d AND lastcid > %d ORDER BY aid DESC LIMIT %d) AS c \
LEFT JOIN \
(SELECT `userid`,`username` FROM `member_info`) as m \
ON c.userid=m.userid \
" % (aid,lastcid,neednum))
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)
        
        db_re_rowcount=self.db.rowcount
        db_re=self.db.fetchall()
        
        senddic={
            'type':'7_com_num',
            'comnum':db_re_rowcount
        }
        self.sendmessage(senddic)
        dic=self.getmessage()
        if(not(dic['reply'])):
            return 0

        fot i in db_re:
            content=i['content']
            aid=i['aid']
            cid=i['cid']
            userid=i['userid']
            username=i['username']
            senddic={
                'aid':aid,
                'cid':cid,
                'userid':userid,
                'content':content,
                'username':username
            }
            self.sendmessage(senddic)
        dic=self.getmessage()
        if(not(dic['reply'])):
            return 0

        return 1
