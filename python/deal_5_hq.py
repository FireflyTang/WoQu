# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_5_hq(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):

        userid=int(self.recvdic['userid'])
        aid=int(self.recvdic['aid'])

        sql=("SELECT * FROM `activity_list` WHERE aid=%d LIMIT 1" % aid)
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)

        db_re=self.db.fetchone()

        fqruserid=db_re['fqruserid']
        form=db_re['form']
        title=db_re['title']
        starttime=db_re['starttime']
        lasttime=db_re['lasttime']
        place=db_re['place']
        peopleneed=db_re['peopleneed']
        peopleapply=db_re['peopleapply']
        peoplein=db_re['peoplein']
        description=db_re['description']
        dz=db_re['dz']
        inserttime=db_re['inserttime']
        portraitmd5=db_re['portraitmd5']

        applymd5=-1
        inmd5=-1
        applyid=-1
        inid=-1

        if(peopleapply):
            sql=('''SELECT group_concat(portraitmd5),group_concat(userid) FROM 
(SELECT * FROM (SELECT * FROM `activity_apply` WHERE aid=%d AND isin=0) AS b LIMIT 3 ) AS c'''  % aid)
            self.log.write("sql: %s\n" % sql)
            self.db.execute(sql)
            db_re=self.db.fetchone()
            applymd5=db_re['group_concat(portraitmd5)']
            applyid=db_re['group_concat(userid)']

        if(peoplein):
            sql=('''SELECT group_concat(portraitmd5),group_concat(userid) FROM 
(SELECT * FROM (SELECT * FROM `activity_apply` WHERE aid=%d AND isin=1) AS b LIMIT 3 ) AS c''' % aid)
            self.log.write("sql: %s\n" % sql)
            self.db.execute(sql)
            db_re=self.db.fetchone()
            inmd5=db_re['group_concat(portraitmd5)']
            inid=db_re['group_concat(userid)']

        isapply=0
        isin=0
        sql=("SELECT `isin` FROM `activity_apply` WHERE aid=%d AND userid=%d LIMIT 1" % (aid,userid))
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)
        if(self.db.rowcount):
            isin=self.db.fetchone()['isin']
            if(isin):
                isapply=0
            else:
                isapply=1
        
        senddic={
            'type':'5_hdxq',
            'userid':fqruserid,
            'form':form,
            'title':title,
            'start':starttime,
            'last':lasttime,
            'place':place,
            'neednum':peopleneed,
            'applynum':peopleapply,
            'innum':peoplein,
            'des':description,
            'applymd5':applymd5,
            'inmd5':inmd5,
            'applyid':applyid,
            'inid':inid,
            'isin':isin,
            'isapply':isapply,
            'publishtime':inserttime,
            'portraitmd5':portraitmd5
        }
        self.sendmessage(senddic)
        return 1
