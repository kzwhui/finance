#!/usr/bin/python
#encoding=utf8

'''
对邮件操作进行简单的封装，满足日常应用
'''

import sys
import smtplib
from email.mime.text import MIMEText
sys.path.append('../conf')
from log import logger
from conf import g_conf

class MailWrapper:
    @staticmethod   # subtype = plain，表示发送纯文本, = html，表示发送网页
    def send_mail(receivers, subject, content, subtype = 'plain'):
        sender = g_conf.MAIL_CONF['email']
        message = MIMEText(content, subtype, 'utf-8')
        message['Subject'] = subject
        message['From'] = '我<' + sender + '>'
        message['To'] = ';'.join(receivers)
        logger.debug('mail message=%s' % message)

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(g_conf.MAIL_CONF['host'], g_conf.MAIL_CONF['port'])
            smtpObj.login(g_conf.MAIL_CONF['user'], g_conf.MAIL_CONF['passwd'])
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.close()
            logger.info('suc to send a mail')
            return True
        except smtplib.SMTPException, e:
            logger.error('fail to send a mail, sender=%s, receivers=%s, error msg=%s' % (sender, receivers, e))
            return False

#######################################################################
def do_test():
    receivers = ['xxxx@163.com']
    subject = '上班通知'
    content = '今天不上班'

    MailWrapper.send_mail(receivers, subject, content)

if __name__ == '__main__':
    do_test()