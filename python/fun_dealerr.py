# -*- coding: utf-8 -*
#!/usr/bin/python
import _thread
import smtplib
from email.mime.text import MIMEText
import time

def dealerr(threadid,title,content):
    fp=open('./log/errlog.log','a')
    fp.write('---------------------------------------\n')
    fp.write("%s : start to deal err \n" % threadid)
    now=time.strftime('%Y-%m-%d-%H-%M-%S\n',time.localtime(time.time()))
    fp.write('time : '+now+'\n')
    fp.write('thread id : %s \n' % threadid)
    fp.write('title : '+title+'\n')
    fp.write('content : '+content+'\n')
    #senderrmail(title,content)


def senderrmail(title,content):

    threadid=_thread.get_ident()

    print(threadid,":","send err email title : ",title)

    account="fireflytang1993@gmail.com"
    password=""

    server = smtplib.SMTP('smtp.gmail.com' )
    server.docmd("EHLO server" )
    server.starttls()
    server.login(account,password)

    msg = MIMEText(content )

    msg['Content-Type' ]='text/plain; charset="utf-8"'
    msg['Subject' ] = title

    msg['From' ] = account
    msg['To' ] = account

    server.sendmail(account, account ,msg.as_string())
    server.close()
