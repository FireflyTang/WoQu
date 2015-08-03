#-*- encoding:utf-8 -*-
import socket
import _thread,threading,time

sockIndex = 1

def connToServer ():
    global sockIndex
    #创建一个socket连接到127.0.0.1:8081，并发送内容
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("127.0.0.1", 4321))
    conn.send("type=1_0&name=hello".encode('utf-8'))
    print(sockIndex)
    sockIndex = sockIndex + 1
    while True:
    #等待服务端返回数据，并输出
        rev = conn.recv(1024)
        print( 'get server msg:' + str(rev))
        break

threads = []
times = 2000
#并发
time1= time.time()
for i in range(0,times):
    t = threading.Thread(target=connToServer())
    threads.append(t)
for i in range(0,times):
    threads[i].start()
for i in range(0,times):
    threads[i].join()
time2= time.time()
print(time2-time1)



