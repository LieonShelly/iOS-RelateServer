import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
ACCESS_EXPIRES = datetime.timedelta(weeks=4)

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	JWT_SECRET_KEY = SECRET_KEY
	JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
	JWT_HEADER_TYPE = None
	JWT_BLACKLIST_ENABLED = True
	JWT_BLACKLIST_TOKEN_CHECKS = ['access']
	UPLOADED_FILES_DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'Files')
	FILE_TEMPLATE_DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'Files' + os.sep + 'template')
	UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'Files')
	UPLOADS_DEFAULT_DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'Files')
	UPLOADED_IMAGES_DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'Files' + os.sep + 'images')
	UPLOADED_DOCUMENT_DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'Files' + os.sep + 'document')
	BASE_DIR = basedir
	ALLOWED_EXTENSIONS = set(['pdf'])
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024
	REDIS_PASSWORD = None
	JSPUSH_APP_KEY = "a639eba745bb34ae8d05ea41"
	JPUSH_MASTER_KEY = "0e8d2f631ac3c4b302485c24"
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'lieoncx@163.com'
	MAIL_PASSWORD = 'auth1992316'
	FLASKY_MAIL_SUBJECT_PREFIX = '[Lieon]'
	FLASKY_MAIL_SENDER = 'lieoncx@163.com'


class DevelopmentConfig(Config):
	DEBUG = True
	MONGODB_DB = 'ios_bai_bao'
	MONGODB_PORT = 27017
	MONGODB_HOST = '127.0.0.1'
	# MONGO_URI = "mongodb://lieon:lieon1992316@localhost:27017/ios_bai_bao"
	MONGO_URI = "mongodb://localhost:27017/ios_bai_bao"
	REDIS_HOST = '127.0.0.1'
	REDIS_PORT = 6379
	# MONGODB_USERNAME = "lieon"
	# MONGODB_PASSWORD = "lieon1992316"


class TestingConfig(Config):
	TESTING = True

class ProductionConfig(Config):
	MONGODB_DB = 'ios_bai_bao'
	MONGODB_PORT = 27017
	MONGODB_HOST = '127.0.0.1' 
	MONGO_URI = "mongodb://lieon:lieon1992316@localhost:27017/ios_bai_bao"
	REDIS_HOST = '127.0.0.1'
	REDIS_PORT = 6379
	MONGODB_USERNAME = "lieon"
	MONGODB_PASSWORD = "lieon1992316"

class CeleryConfig:
	broker_url = 'redis://localhost:6379/2'
	result_backend = 'mongodb://lieon:lieon1992316@localhost:27017/ios_bai_bao_celery_task'
	imports = ('App.CeleryTask')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}

class RedisDBConfig:
	company =  os.environ.get('SECRET_KEY') + "company"
	user_info =  os.environ.get('SECRET_KEY') + "user_info"
	company_info =  os.environ.get('SECRET_KEY') + "company_info"
	dealer_company_info =  os.environ.get('SECRET_KEY') + "dealer_company_info"
	platform_user_info =  os.environ.get('SECRET_KEY') + "platform_user_info"
	article_like_key =  os.environ.get('SECRET_KEY') + "article_like_key"
	article_comment_key =  os.environ.get('SECRET_KEY') + "article_comment_key"
	comment_reply_key =  os.environ.get('SECRET_KEY') + "comment_reply_key"
	sso_key = os.environ.get('SECRET_KEY') + "sso_key"
	verify_code_num_key = os.environ.get('SECRET_KEY') + "verify_code_num_key"
	article_is_like_key = os.environ.get('SECRET_KEY') + "article_is_like_key" #是否点赞
	article_message_unread_key = os.environ.get('SECRET_KEY') + "article_message_unread_key" # 说说消息未读数