# -*- coding: utf-8 -*
#!/usr/bin/python
import urllib.parse 

#string->bytes:decode(str,'utf-8')
#bytes->string:encode(str,'utf-8')


def message2dic(message):
    #message='TYPE=1_1&name=%E4%BD%A0%26%E5%A5%BD'
    #将消息按url拆成不同的字段，自动完成转义，返回值为字典，key=>value value为列表
    dic= urllib.parse.parse_qs(message,True)
    #将value转化为字符串
    for i in dic:
        dic[i]=''.join(dic[i])

    #前两个字段转化为数字
    #dic['TYPE']=int(dic['TYPE'])
    #dic['SUBTYPE']=int(dic['SUBTYPE'])

    return dic

def dic2message(dic):
    #print(urlencode(dic))
    return urllib.parse.urlencode(dic)




