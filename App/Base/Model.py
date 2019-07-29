from App import db
from Utils.DateTimeTool import return_time_now

class DocumentStatus:
    DELETEED = 0
    NORMAL = 1
    EXCEPTION = 2

class BaseDocument(object):
    create_time = db.IntField(default=return_time_now)
    modify_time = db.IntField(default=return_time_now)
    status = db.IntField(default=DocumentStatus.NORMAL, choices=(DocumentStatus.NORMAL, DocumentStatus.DELETEED, DocumentStatus.EXCEPTION))  # 0.删除 1.正常, 2. 异常


class BaseEmbeddedDocument(object):
    create_time = db.IntField(default=return_time_now)
    modify_time = db.IntField(default=return_time_now)
    status = db.IntField(default=1)  # 0.删除 1.正常
