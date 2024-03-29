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
    return thr

