from .Model import VerificationCode, MailMessage
import random
from App.Log import logger
from Utils.Email import send_email

#  发送验证码
def send_verifycode(body):
    code=str(random.randint(100000, 999999))
    to_email = body.get('to_email')
    db_code = VerificationCode()
    db_code.email = to_email
    db_code.code = code
    try:
        db_code.save()
        send_email(to_email, '验证码', 'Mail/VerifyCode', code = code)
        return True, {}
    except Exception as e:
        logger.exception(e)
        return False, "异常"


# 发送消息
def send_mssage(body):
    title = body.get('title')
    content = body.get('content')
    to_email = body.get('to_email')
    message = MailMessage()
    message.title = title
    message.content = content
    message.email = to_email
    # message.save()
    send_email(to_email, '消息', 'Mail/AlertMessage', message = message)
    return True, {}
