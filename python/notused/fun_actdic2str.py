#coding: utf-8
#!/usr/bin/python

def actdic2str(actdic):
    s=''
    for(i in actdic):
        s.join((("%s|") % actdic[i]))
    return s[:-1]
