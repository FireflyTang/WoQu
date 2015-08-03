# -*- coding: utf-8 -*
#!/usr/bin/python

from dealctrl import *

class deal_3_cfr(dealctrl):
    def __init__(self,con):
        dealctrl.__init__(self,con)
    def run(self):
        basename=self.recvdic['md5']
        issendok=self.sendfile(basename)
        return issendok
