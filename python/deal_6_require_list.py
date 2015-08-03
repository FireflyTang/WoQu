# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *
from fun_activity import *
import time

class deal_6_require_list(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        anum=int(self.recvdic['anum'])
        order=int(self.recvdic['order'])
        needlistnum=int(self.recvdic['needlistnum'])
        
        sqlyear=''
        sqlgender=''
        sqldate=''
        sqlperiod=''
        sqldepartment=''
        sqlpeople=''
        sqlform=''

        if(self.recvdic['date']):
            sqldate=(" (%s)" % multi2str('date',self.recvdic['date']))
        else:
            sqldate=(' (starttime > %d)' % self.now)

        maxpeople=self.recvdic['maxpeople']
        minpeople=self.recvdic['minpeople']
        if(maxpeople and minpeople):
            sqlpeople=(" AND (peopleneed<=%s AND peopleneed>=%s)" % (maxpeople,minpeople))
        if(maxpeople and not(minpeople)):
            sqlpeople=(" AND peopleneed<=%s" % maxpeople)
        if(minpeople and not(maxpeople)):
            sqlpeople=(" AND peopleneed>=%s" % minpeople) 

        if(self.recvdic['period']):
            sqlperiod=(" AND (%s)" % multi2str('period',self.recvdic['period']))
        if(self.recvdic['form']):
            sqlform=(" AND form= %s" % self.recvdic['form'])
  
        if(self.recvdic['year']):
            sqlyear=("AND year= %s" % self.recvdic['year'])
        if(self.recvdic['gender']):
            sqlgender=("AND gender= %s" % self.recvdic['gender'] )
        if(self.recvdic['department']):
            sqldepartment=("AND department= %s" % self.recvdic['department'])
        
        sqlorder=order2str(order)
        sqllimit=('LIMIT %d,%d' % (anum,needlistnum))
        
        inner_sql_header=("SELECT * FROM `activity_list` WHERE")
        inner_sql=''.join((inner_sql_header,sqldate,sqlpeople,sqlperiod,sqlform))
        sql=('''
SELECT * FROM (%s) AS a 
LEFT JOIN (SELECT * FROM `activity_dz` WHERE dz_userid=%d) AS dz 
ON a.aid=dz.dz_aid 
LEFT JOIN (SELECT * FROM `member_sc` WHERE sc_userid=%d) AS sc 
ON a.aid=sc.sc_aid 
LEFT JOIN 
(SELECT * FROM `member_pb` WHERE pb_userid=%d) AS pb 
ON a.aid=pb.pb_aid 
LEFT JOIN 
(SELECT `userid`,`username`,`gender`,`portraitmd5`,`year`,`department`,`edutype` FROM `member_userinfo`) AS name 
ON name.userid=a.fqruserid 
WHERE (pb.pb_userid IS NULL) %s %s %s 
%s %s 
''' % (inner_sql,userid,userid,userid,sqlyear,sqlgender,sqldepartment,sqlorder,sqllimit))
        self.log.write("sql: %sn" % sql)
        self.db.execute(sql)

        db_re=self.db.fetchall()
    
        aidlist=[]
        for i in db_re:
            aidlist.append(str(i['aid']))

        length=len(aidlist)
        if(length):
            senddic={
                'type':'6_aid_list',
                'count':length,
                'aidlist':','.join(aidlist)
                }
        else:
            senddic={
                'type':'6_aid_list',
                'count':0,
                'aidlist':-1
                }
        self.sendmessage(senddic)

        dic=self.getmessage()
        aidlistorder=[]
        if(dic['aidlistorder']):
            aidlistorder=dic['aidlistorder'].split(',')
        for i in aidlistorder:
            i=int(i)
            ainfo=db_re[i]
            
            if(ainfo['dz_userid']):
                isdz=1
            else:
                isdz=0
            if(ainfo['sc_userid']):
                issc=1
            else:
                issc=0
            
            aid=ainfo['aid']
            fqruserid=ainfo['fqruserid']
            username=ainfo['username']
            gender=ainfo['gender']
            portraitmd5=ainfo['portraitmd5']
            year=ainfo['year']
            department=ainfo['department']
            title=ainfo['title']
            starttime=ainfo['starttime']
            dz=ainfo['dz']
            peopleapply=ainfo['peopleapply']
            peopleneed=ainfo['peopleneed']
            peoplein=ainfo['peoplein']
            edutype=ainfo['edutype']
            inserttime=ainfo['inserttime']
        
            senddic={
            'type':'6_alistinfo',
            'aid':aid,
            'userid':fqruserid,
            'username':username,
            'gender':gender,
            'portraitmd5':portraitmd5,
            'edutype':edutype,
            'year':year,
            'department':department,
            'title':title,
            'starttime':starttime,
            'dzcount':dz,
            'neednum':peopleneed,
            'innum':peoplein,
            'applynum':peopleapply,
            'isdz':isdz,
            'issc':issc,
            'publishtime':inserttime
            }
            self.sendmessage(senddic)
        dic=self.getmessage()
        if(not(dic['reply']=='1')):
            return 0
        return 1
           
        
