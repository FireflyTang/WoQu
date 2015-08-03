# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *
from fun_activity import *

class deal_5_fqhd(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):

        userid=int(self.recvdic['userid'])
        form=int(self.recvdic['form'])
        title=self.recvdic['title']
        starttime=int(self.recvdic['start'])
        lasttime=int(self.recvdic['last'])
        place=self.recvdic['place']
        peopleneed=int(self.recvdic['neednum'])
        description=self.recvdic['des']

        period=starttime2period(starttime)
        date=starttime2date(starttime)
        weekday=starttime2weekday(starttime)
        
        sql=("SELECT `portraitmd5` FROM `member_userinfo` WHERE userid=%d LIMIT 1" % userid)
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)
        portraitmd5=self.db.fetchone()['portraitmd5']

        sql=("INSERT INTO `activity_list`(`fqruserid`,`portraitmd5`, `form`, `title`, `inserttime`, `amodifytime`,`starttime`, `lasttime`, `period`,`date`,`weekday`, `place`, `peopleneed`, `description`) VALUES (%d,'%s',%d,'%s',%d,%d,%d,%d,%d,%d,%d,'%s',%d,'%s')" % (userid,portraitmd5,form,title,self.now,self.now,starttime,lasttime,period,date,weekday,place,peopleneed,description))
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)

        senddic={
            'type':'5_r',
            'reply':1,
            'publishtime':self.now
        }
        self.sendmessage(senddic)
        return 1
