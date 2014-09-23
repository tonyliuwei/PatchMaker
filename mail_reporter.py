#!/usr/bin/env python
# -*- coding: utf-8 -*-
#导入smtplib和MIMEText
import smtplib,sys 
from email.mime.text import MIMEText 
def send_mail(sub,content): 
#############
#要发给谁，这里发给1个人
    mailto_list=["lwei@jzby.com"] 
#####################
#设置服务器，用户名、口令以及邮箱的后缀
    mail_host="192.168.6.49"
    mail_user="lwei"
    #mail_pass=""
    mail_postfix="jzby.com"
######################
    '''''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
    '''
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    #me='llhui'+"<"+'llhui'+"@"+mail_postfix+">"
    #print me
    msg = MIMEText(content,_charset='UTF-8') 
    msg.set_charset('UTF-8')
    msg['Subject'] = sub 
    msg['From'] = me 
    msg['To'] = ";".join(mailto_list) 
    try: 
        s = smtplib.SMTP() 
        s.connect(mail_host) 
        print 'connect'
        #s.login(mail_user,mail_pass) # this mail server doesn't need login
        #print 'login'
        s.sendmail(me, mailto_list, msg.as_string()) 
        s.close() 
        return True
    except Exception, e: 
        print str(e) 
        return False
if __name__ == '__main__': 
    if send_mail(u'PatchMaker',u'python mail'): 
        print 'good'
    else: 
        print 'bad'