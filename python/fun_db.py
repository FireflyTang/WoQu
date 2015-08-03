# -*- coding: utf-8 -*
#!/usr/bin/python

import pymysql
import _thread
import time
db_host='127.0.0.1'
db_username='root'
db_password='woqu'
db_name='woqu'
db_port=3306

pingtime=300

#数据库控制类
def db_cursor_list_init(db_cursor_num,mainlog):
    #游标列表
    db_cursor_list=[]
    #连接列表
    db_con_list=[]
    for i in range(0,db_cursor_num):
        contemp=pymysql.connect(host=db_host,user=db_username,passwd=db_password,db=db_name,port=db_port,charset='utf8')
        contemp.autocommit(True)
        db_con_list.append(contemp)
        db_cursor_list.append(db_con_list[i].cursor(pymysql.cursors.DictCursor))
    #新建线程来定时ping
    _thread.start_new_thread(db_keppcon_thread,(db_cursor_num,db_con_list,mainlog))
    return db_cursor_list


def db_keppcon_thread(db_cursor_num,db_con_list,mainlog):
    while True:
        db_keppcon(db_cursor_num,db_con_list,mainlog)
        time.sleep(pingtime)
def db_keppcon(db_cursor_num,db_con_list,mainlog):
    #mainlog.write("ping mysql\n")
    for i in range(0,db_cursor_num):
        db_con_list[i].ping()
    


        
