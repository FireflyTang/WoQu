# -*- coding: utf-8 -*
#!/usr/bin/python
import time

def starttime2period(starttime):
    t=time.gmtime(starttime+28800)
    h=t.tm_hour
    if(h<11): return 1
    if(h<13): return 2
    if(h<18): return 3
    return 4
def starttime2date(starttime):
    return int(time.strftime("%Y%m%d",time.gmtime(starttime+28800)))

def multi2str(prefix,date):
    date=date.split(",")
    datestr=[]
    for i in date:
        datestr.append("%s=%s" % (prefix,i))
    return ' OR '.join(datestr)

def order2str(order):
    if(order==0): return 'ORDER BY starttime'
    if(order==1): return 'ORDER BY starttime'
    if(order==2): return 'ORDER BY dz DESC'
    if(order==3): return 'ORDER BY peopleneed DESC'
    if(order==4): return 'ORDER BY peoplein DESC'

def starttime2weekday(starttime):
    s=time.gmtime(starttime+28800)
    return s.tm_wday
    
