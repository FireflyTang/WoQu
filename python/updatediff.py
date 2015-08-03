# -*- coding: utf-8 -*
#!/usr/bin/python

import pymysql
import shutil
import os
import subprocess
from fun_update import *
import time

newversion=3
filepath="./temp/woqu3.apk"
isforce=1

db_host='127.0.0.1'
db_username='root'
db_password=''
db_name='woqu'
db_port=3306

bsdiffpath="bsdiff"

tempfile="./temp/patch"

newmd5=calmd5(filepath)
newsize=calsize(filepath)
newpath=("./files/update/%s.apk" % newmd5)
shutil.copyfile(filepath,newpath)

con=pymysql.connect(host=db_host,user=db_username,passwd=db_password,db=db_name,port=db_port,charset='utf8')
con.autocommit(True)
c=con.cursor(pymysql.cursors.DictCursor)


sql=("SELECT * FROM `update_version` ORDER BY version DESC")
print(sql)
c.execute(sql)
oldinfo=c.fetchall()
print(oldinfo)

sql=("INSERT INTO `update_version` (`version`,`fullsize`,`md5`,`releasetime`) VALUES (%d,%d,'%s',%d)" \
% (newversion,newsize,newmd5,int(time.time())))
print(sql)
c.execute(sql)

sql=("INSERT INTO `file_filerecord`(`basename`, `extname`, `fileclass`, `uploadtime`) VALUES ('%s','%s','%s',%d)" \
% (newmd5,'apk','update',time.time()))
c.execute(sql)
print(sql)


for i in range(0,len(oldinfo)):
    print('--------------------------------')
    print('i=',i)
    a=oldinfo.pop(0)
    print(a)
    oldmd5=a['md5']
    oldversion=a['version']
    oldpath=("./files/update/%s.apk" % oldmd5)
    print('old version: ',oldversion)
    command=bsdiffpath+(" %s %s %s" % (oldpath,newpath,tempfile))
    print(command)
    handle = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    result=handle.communicate()[0].decode('utf-8')
    excode=handle.returncode
    assert(excode==0)

    patchmd5=calmd5(tempfile)
    patchsize=calsize(tempfile)
    patchpath=("./files/update/%s.p" % (patchmd5))
    shutil.move(tempfile,patchpath)
    sql=("INSERT INTO `update_info`(`newversion`, `oldversion`, `newmd5`, `oldmd5`,`fullsize`, `patchmd5`, `patchsize`, `isforce`, `releasetime`) VALUES (%d,%d,'%s','%s',%d,'%s',%d,%d,%d)" % (newversion,oldversion,newmd5,oldmd5,newsize,patchmd5,patchsize,isforce,time.time()))
    c.execute(sql)
    print(sql)
    sql=("INSERT INTO `file_filerecord`(`basename`, `extname`, `fileclass`, `uploadtime`) VALUES ('%s','%s','%s',%d)" \
% (patchmd5,'p','update',time.time()))
    c.execute(sql)
    print(sql)
    
    print('--------------------------------')
c.close()
    
