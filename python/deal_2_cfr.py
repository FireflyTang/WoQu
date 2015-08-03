#-*- coding: utf-8 -*
#!/usr/bin/python
from dealctrl import *

class deal_2_cfr(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        
        userid=int(self.recvdic['userid'])
        basename=self.recvdic['md5']
        extname=self.recvdic['extension']
        fileclass=self.recvdic['class']
        filesize=int(self.recvdic['size'])
        re=self.getfile(basename,extname,fileclass,filesize)
        if(re):
            if(fileclass=='portrait'):
                sql=("UPDATE `member_userinfo` SET `portraitmd5`='%s' WHERE userid=%d" % (basename,userid))
                self.log.write("sql: %s\n" % sql)
                self.db.execute(sql)
        return re    
                
