#coding: utf-8
#!/usr/bin/python
#coding: utf-8
#结构:main->threadpool->conthread->conctrl->newcon->dealctrl->deal->con->sendmessage

recvmessagemaxsize=1024
filepackagemaxsize=10240
timeout=5

from fun_messagedic import *
import _thread
import os
from hashlib import md5
import time 
import ipaddress
import socket

#连接控制父类
class conctrl:
    #获取套接字与地址
    def __init__(self,connection,address,db_cursor,threadlog):
        global timeout
        self.connection=connection
        self.address=address
        self.connection.setblocking(True)
        #self.connection.settimeout(timeout)
        #数据库游标
        self.db_cursor=db_cursor 
        #日志
        self.threadlog=threadlog

        self.recvcache=''
    #断开连接
    def close(self):
        self.connection.close()
    #获取消息并转化为dic
    def getmessage(self):
        global timeout
        time0=time.time()
        #消息传送规范 备选升级版
        while True:
            try:
                pos=self.recvcache.index('|')
                break
            except ValueError:
                if(time.time()-time0)>timeout: raise socket.timeout 
                arecv=self.connection.recv(recvmessagemaxsize)
                if(not(arecv)):
                    continue
                self.threadlog.write("read from buffer: %s\n" % arecv)                         
                #由bytes到str
                arecv=arecv.decode('utf-8')
                #去除字符串最后的\n等
                #if[-1]=='\n'):
                #    tempmessage=tempmessage[:-1]
                self.recvcache+=arecv
        message=self.recvcache[:pos]
        self.threadlog.write("recvcache before read message: %s\n" % self.recvcache)
        self.recvcache=self.recvcache[pos+1:]
        self.threadlog.write('message: %s\n' % message)
        '''
        #原来的消息传送规范
        message=self.connection.recv(recvmessagemaxsize)
        self.threadlog.write('recv: %s\n' % message)
        message=message.decode('utf-8')
        '''
        #if(message[-1]=='\n'):
        #    message=message[:-1]
        #数据完整性由TCP协议保证，但保留SIZE字段
        dic=message2dic(message)
        return dic
        
    #从dic转化为消息并发出
    def sendmessage(self,dic):
        #给java发信息需要加\r\n,str到bytes
        message=(dic2message(dic)+'\r\n').encode('utf-8')
        self.threadlog.write("send message : %s\n" % message)
        messagelen=self.connection.send(message)
        self.threadlog.write("successfully send message size : %d\n" % messagelen)
        return messagelen

    #接收文件
    def getfile(self,basename,extname,fileclass,filesize):
        #打开文件准备接受
        filemd5=md5();
        prefix=''
        path=("./files/%s%s.%s" % (prefix,basename,extname))
        
        sql=("SELECT * FROM `file_filerecord` WHERE basename='%s' LIMIT 1" % basename)
        self.threadlog.write("sql : %s\n" % sql)
        self.db_cursor.execute(sql)
        if(self.db_cursor.rowcount):
            senddic={
                'type':'2_sr',
                'reply':2
                }
            self.sendmessage(senddic)
            return 2
        
        try:
            newfile=open(path,'wb+')
            self.threadlog.write('start to get file : %s\n' % path)        
            #可以开始接收
            senddic={
                'type':'2_sr',
                'reply':1
                }
            self.sendmessage(senddic)
            #开始接收
            size=0;
            while(size<filesize):
                recvfiledata=self.connection.recv(filepackagemaxsize)
                if(not(recvfiledata)):
                    break
                packagesize=len(recvfiledata)
                self.threadlog.write('get file package = %d\n' % packagesize)
                size+=len(recvfiledata)
                filemd5.update(recvfiledata)
                newfile.write(recvfiledata)
        finally:
            newfile.close()
        filemd5=filemd5.hexdigest()
        self.threadlog.write('file basename actually is : %s\n' % basename)
        self.threadlog.write('received file md5 is : %s\n' % filemd5)
        self.threadlog.write('filesize actually is : %d\n' % size)
        #接收错误
        if(not(filemd5==basename)):
            self.threadlog.write('file get err, filename : %s\n' % basename)
            os.remove(path)
            sneddic={
                'type':'2_sr_success',
                'reply':0
                }
            self.sendmessage(sneddic)
            return 0
        #接收正确
        else:
            self.threadlog.write('file get successfully, file path : %s\n' % path)
            #文件记录到数据库
            sql=("INSERT INTO `file_filerecord`(`basename`, `extname`, `fileclass`, `uploadtime`) VALUES ('%s','%s','%s',%d)" % (basename,extname,fileclass,int(time.time())))
            self.threadlog.write("sql : %s\n" % sql)
            self.db_cursor.execute(sql)
            senddic={
                'type':'2_sr_success',
                'reply':1
                }
            self.sendmessage(senddic)
            return 1

    #发送文件
    def sendfile(self,basename):
        #由md5查得文件信息
        sql=("SELECT `extname`, `fileclass` FROM `file_filerecord` WHERE basename='%s' LIMIT 1" % basename)
        self.threadlog.write("sql : %s\n" % sql)
        self.db_cursor.execute(sql)
        db_re=self.db_cursor.fetchone()
        extname=db_re['extname']
        fileclass=db_re['fileclass']
        prefix=''
        if(fileclass=='update'):
            prefix='update/'
        path=("./files/%s%s.%s" % (prefix,basename,extname))
        self.threadlog.write('start to send file : %s\n' % path)
        #分离扩展名
        #name, ext = os.path.splitext(filename)
        #获取文件大小
        filesize=os.path.getsize(path)
        #发送大小与扩展名
        senddic={
            'extension':extname,
            'md5':basename,
            'size':filesize,
            'type':'3_sr'
            }
        self.sendmessage(senddic)
        #接收是否可以发送
        dic=self.getmessage()
        if((dic['reply']=='0') or (not(dic['type']=='3_cp'))):
            return 0
        #打开文件
        try:
            newfile=open(path,'rb')
            #已发送大小
            size=0
            while(size<filesize):
                sendfiledata=newfile.read(filepackagemaxsize);
                if(not(sendfiledata)):
                    break
                packagesize=len(sendfiledata)
                size+=packagesize
                self.threadlog.write('send file package = %d\n' % packagesize)
                self.connection.send(sendfiledata)
        finally:
            newfile.close()
        #显示实际发送大小与应该接收大小
        self.threadlog.write('send filesize should be : %d\n' % filesize)
        self.threadlog.write('send filesize actually is : %d\n' % size)
        dic=self.getmessage()
        if(not(dic['type']=='3_fts')):
            return 0
        issendfileok=int(dic['reply'])
        self.threadlog.write('send file result is : %d\n' % issendfileok)
        return issendfileok


class con(conctrl):
    def __init__(self,connection,address,db_cursor,threadlog):
        #初始化父类
        conctrl.__init__(self,connection,address,db_cursor,threadlog)

    #运行处理类
    def run(self):
        self.threadlog.write("connect run\n")

        #获取消息内容       
        self.recvdic=self.getmessage()
        self.threadlog.write("recvdic : %s\n" % self.recvdic)
        
        sql=("INSERT INTO `connect_connect_log`(`connecttime`, `address`, `port`, `userid`) VALUES (%d,%d,%d,%d)" % (int(time.time()),int(ipaddress.IPv4Address(self.address[0])),int(self.address[1]),int(self.recvdic['userid'])))
        self.threadlog.write("sql: %s\n" % sql)
        self.db_cursor.execute(sql)

        '''
        安全性:用户合法性检测,检测token是否与记录相同,放在注册之后
        if(not(checkuser(self.recvdic))):
            抛出异常不合法用户，可于此处返回值，或全局记录防止攻击
            pass
            return notok
        '''
        #动态加载模块
        
        modname=self.recvdic['type']
        i="from deal_"+modname+" import deal_"+modname
        self.threadlog.write("%s\n" % i)
        exec(i)
        exec("self.deal=deal_"+modname+"(self)")
        self.threadlog.write("deal_%s to run\n" % modname)
        if(self.deal.run()):
            self.threadlog.write("deal_%s run successfully\n" % modname)
        else:
            raise Exception
