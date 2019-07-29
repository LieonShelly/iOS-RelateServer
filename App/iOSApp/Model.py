from App import db
from App.Base.Model import BaseDocument

# 验证码
class VerificationCode(BaseDocument, db.Document):
    email = db.StringField()
    code = db.StringField()


# 邮箱消息
class MailMessage(BaseDocument, db.Document):
    title = db.StringField()
    content = db.StringField()
    email = db.StringField()
