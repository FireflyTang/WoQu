# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_1_4(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])

        sql=("SELECT * FROM `member_userinfo` WHERE userid=%d LIMIT 1" % userid)
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)

        db_re=self.db.fetchone()
                
        username=db_re['username']
        portraitmd5=db_re['portraitmd5']                
        gender=db_re['gender']
        department=db_re['department']
        year=db_re['year']
        edutype=db_re['edutype']
        state=db_re['state']
        mobile=db_re['mobile']
        mail=db_re['mail']
        personalsign=db_re['personalsign']
        
        senddic={
            'type':'1_4_r',
            'reply':1,
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
