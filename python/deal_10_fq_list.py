# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_10_pb_list(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        time=int(self.recvdic['time'])
        timelimit=''
        if(time):
            timelimit=('AND fq_dateline<=%d' % (time))
            
        sql=('''SELECT * FROM 
(SELECT * FROM `member_pb`  WHERE  pb_userid=%d %s LIMIT 10) AS a
LEFT JOIN 
`activity_list`  AS b
ON a.pb_aid=b.aid
LEFT JOIN
`member_userinfo` AS c
ON b.fqruserid=c.userid
LEFT JOIN 
(SELECT * FROM `member_sc` WHERE sc_userid=%d) AS d
ON a.pb_aid=d.sc_aid
LEFT JOIN 
(SELECT * FROM `activity_dz` WHERE dz_userid=%d) AS e
ON a.pb_userid=e.dz_userid
LEFT JOIN 
(SELECT * FROM `activity_apply` WHERE userid=%d) as f
ON a.pb_aid=f.userid
ORDER BY pb_dateline DESC
LIMIT 10''' % (userid,timelimit,userid,userid,userid))

        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)

        db_re_rowcount=self.db.rowcount
        db_re=self.db.fetchall()

        amodifytime=[]
        umodifytime=[]
        aid=[]
        userid=[]
        for i in db_re:
            amodifytime.append(str(i['amodifytime']))
            umodifytime.append(str(i['amodifytime']))
            aid.append(str(i['aid']))            
            userid.append(str(i['userid']))
        amodifytime=','.join(amodifytime)
        umodifytime=','.join(umodifytime)
        aid=','.join(aid)
        userid=','.join(userid)

        senddic={
            'type':'10_pb_list_r',
            'count':db_re_rowcount,
            'aid':aid,
            'userid':userid,
            'amodifytime':amodifytime,
            'umodifytime':umodifytime
            }
        self.sendmessage(senddic)
        
        dic=self.getmessage()
        uorder=dic['uorder']
        aorder=dic['aorder']
        if(aorder):
            aorder=aorder.split(',')
            for i in aorder:
                i=int(i)
                ainfo=db_re[i]
                form=ainfo['form']
                title=ainfo['title']
                starttime=ainfo['starttime']
                lasttime=ainfo['lasttime']
                publishtime=ainfo['inserttime']
                aid=ainfo['aid']
                place=ainfo['place']
                description=ainfo['description']
                fqruserid=ainfo['fqruserid']
                dz=ainfo['dz']
                peopleneed=ainfo['peopleneed']
                peopleapply=ainfo['peopleapply']
                peoplein=ainfo['peoplein']
                ispb=1
                if(ainfo['sc_dateline']):
                    issc=1
                else:
                    issc=0
                if(ainfo['dz_dateline']):
                    isdz=1
                else:
                    isdz=0
                if(ainfo['applytime']):
                    isapply=1
                else:
                    isapply=0
                if(ainfo['isin']=='1'):
                    isapply=0
                    isin=1
                else:
                    isin=0
                pbtime=ainfo['pb_dateline']

                applymd5=-1
                inmd5=-1
                applyid=-1
                inid=-1

                if(peopleapply):
                    sql=('''SELECT group_concat(portraitmd5),group_concat(userid) FROM 
(SELECT * FROM (SELECT * FROM `activity_apply` WHERE aid=%d AND isin=0) LIMIT 3) AS c''' % aid)
                    self.log.write("sql: %s\n" % sql)
                    self.db.execute(sql)
                    db_re=self.db.fetchone()
                    applymd5=db_re['group_concat(portraitmd5)']
                    applyid=db_re['group_concat(userid)']

                if(peoplein):
                    sql=('''SELECT group_concat(portraitmd5),group_concat(userid) FROM 
( SELECT * FROM (SELECT * FROM `activity_apply` WHERE aid=%d AND isin=1) LIMIT 3 ) AS c''' % aid)
                    self.log.write("sql: %s\n" % sql)
                    self.db.execute(sql)
                    db_re=self.db.fetchone()
                    inmd5=db_re['group_concat(portraitmd5)']
                    inid=db_re['group_concat(userid)']

                senddic={
                    'type':'10_pb_list_a',
                    'form':form,
                    'title':title,
                    'starttime':starttime,
                    'lasttime':lasttime,
                    'publishtime':publishtime,
                    'aid':aid,
                    'place':place,
                    'des':description,
                    'userid':fqruserid,
                    'dz':dz,
                    'neednum':peopleneed,
                    'applynum':peopleapply,
                    'innum':peoplein,
                    'ispb':ispb,
                    'issc':issc,
                    'isdz':isdz,
                    'applymd5':applymd5,
                    'applyid':applyid,
                    'inmd5':inmd5,
                    'inid':inid,
                    'isin':isin,
                    'isapply':isapply,
                    'pbtime':pbtime
                    }  
                self.sendmessage(senddic)
        if(uorder):
            for i in uorder:
                i=int(i)
                uinfo=db_re[i]
                fqruserid=uinfo['fqruserid']
                username=uinfo['username']
                portraitmd5=uinfo['portraitmd5']
                gender=uinfo['gender']
                department=uinfo['department']
                year=uinfo['year']
                edutype=uinfo['edutype']
                mobile=uinfo['mobile']
                mail=uinfo['mail']
                personalsign=uinfo['personalsign']
                senddic={
                    'type':'type=10_pb_list_u',
                    'userid':fqruserid,
                    'username':username,
                    'portraitmd5':portraitmd5,
                    'gender':gender,
                    'department':department,
                    'year':year,
                    'edutype':edutype,
                    'mobile':mobile,
                    'mail':mail,
                    'personalsign':personalsign
                    }
                self.sendmessage(senddic)
        return 1
