# -*- coding: utf-8 -*
#!/usr/bin/python

import pymysql
import _thread
import time
from hashlib import md5
import os

def calmd5(path):
    fp=open(path,'rb')
    filemd5=md5()
    while(1):
        temp=fp.read(10240)
        if(not(temp)):
            break
        filemd5.update(temp)
    fp.close()
    filemd5=filemd5.hexdigest()
    return filemd5

def calsize(path):
    return os.path.getsize(path)
