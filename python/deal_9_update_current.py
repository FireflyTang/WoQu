# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_9_update_current(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        userid=int(self.recvdic['userid'])
        version=int(self.recvdic['version'])
        
        sql=("SELECT MAX(version),`fullsize` FROM `update_version`")
        self.log.write("sql: %s\n" % sql)
        self.db.execute(sql)
        db_re=self.db.fetchone()
        lastest=db_re['MAX(version)']
        
        fullsize=0
        patchsize=0
        
        reply=0
        if(not(version==lastest)):
            reply=1
            sql=("SELECT * FROM `update_info` WHERE newversion=%d AND oldversion=%d LIMIT 1" % (lastest,version))
            self.log.write("sql: %s\n" % sql)
            self.db.execute(sql)
            db_re=self.db.fetchone()
            isforce=db_re['isforce']
            newmd5=db_re['newmd5']
            oldmd5=db_re['oldmd5']
            patchmd5=db_re['patchmd5']
            patchsize=db_re['patchsize']
            fullsize=db_re['fullsize']
            if(isforce):
                reply=2
        senddic={
            'type':'9_update_current_reply',
            'reply':reply,
            'fullsize':fullsize,
            'patchsize':patchsize
            }
        self.sendmessage(senddic)
        
        dic=self.getmessage()
        if(dic['reply']=='1'):
            senddic={
                'type':'9_update_reply',
                'newmd5':newmd5,
                'patchmd5':patchmd5,
                'fullsize':fullsize,
                'patchsize':patchsize,
                'currentmd5':oldmd5
                }
            self.sendmessage(senddic)

        return 1
