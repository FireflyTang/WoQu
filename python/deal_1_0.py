# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *
from fun_isTsinghua import *

class deal_1_0(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        password=self.recvdic['password']
        
        
        isTsinghuaStudent=isTsinghua(self.recvdic['userid'],self.recvdic['password'])
        if(isTsinghuaStudent):
            #是清华学生
            sql=("SELECT * FROM `member_userinfo` WHERE userid=%d LIMIT 1" % userid)
            self.log.write("sql: %s\n" % sql)
            self.db.execute(sql)
            sql_re_rowcount=self.db.rowcount
            
            '''
            toregister=1
            if (sql_re_rowcount):
                isregistered=self.db.fetchone()['isregistered']
                if (isregistered==1):
                    toregister=0
            '''
            if (sql_re_rowcount):
                #如果已经注册过了，则返回注册结果
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
                    'type':'1_1',
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

            else:
                #如果没有注册过，这次验证通过
                senddic={
                    'type':'1_1',
                    'reply':2
                }
                
        #不是清华学生
        else:
            senddic={
            'type':'1_1',
            'reply':0
               }


        self.sendmessage(senddic)
        return 1
