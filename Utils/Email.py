from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from App import mail
import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(str(app.config['FLASKY_MAIL_SUBJECT_PREFIX']) + ' ' + subject, 
                  sender=app.config['FLASKY_MAIL_SENDER'], 
                  recipients=[to])
    template = render_template(template + '.html', **kwargs)
    msg.html = template
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
#     sendEmail(["454287928@qq.com"], 'hello there, The IPA has a update, please check in')
    return thr


def sendEmail(reciever, messageTile, messageContent):
    hostServer = "smtp.163.com"
    sender = "lieoncx@163.com"
    password = "auth1992316"
    smtp = SMTP_SSL(hostServer)
    smtp.set_debuglevel(1)
    smtp.ehlo(hostServer)
    smtp.login(sender, password)
    message = MIMEText(messgaeContent, "plain", 'utf-8')
    message['Subject'] = Header(messageTile, "utf-8")
    message['From'] = sender
    if len(reciever) > 1:
        message['To'] = ','.join(reciever)
    else:
        message['To'] = reciever[0]
    smtp.sendmail(sender, reciever, message.as_string())
    smtp.quit()
