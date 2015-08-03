# -*- coding: utf-8 -*
#!/usr/bin/python  
  
import urllib.parse
import urllib.request 
import http.cookiejar  
import string  
import re  
def isTsinghua(username,password):
    hosturl = 'http://learn.tsinghua.edu.cn'  

    posturl = 'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp' 
  
    ck =  http.cookiejar.LWPCookieJar()  
    cookie_support = urllib.request.HTTPCookieProcessor(ck)  
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)  
    urllib.request.install_opener(opener)  
  
  
    host = urllib.request.urlopen(hosturl)  
  
 
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',  
               'Referer' : 'http://info.tsinghua.edu.cn/'}  
  
    postData = {'userid':username,
                'userpass':password,
                'submit1':'登录'
                }  


    postData = urllib.parse.urlencode(postData).encode('utf-8')  
  
    request = urllib.request.Request(posturl, postData, headers)

    response = urllib.request.urlopen(request)  
    
    text = response.read().decode('utf-8')

    result=re.search(r"alert",text)

    if(result):
        result=0
    else:
        result=1
    return result


