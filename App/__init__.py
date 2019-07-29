from flask import Flask
from Config import config, CeleryConfig, Config
from flask_uploads import (UploadSet, configure_uploads, IMAGES, DOCUMENTS,
                           UploadNotAllowed, patch_request_class)
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from App.Cache.Service import RedisClient
from flask_cors import *
from App.Log import logger
import jpush
from celery import Celery
from flask_mail import Mail
import os

mongod = PyMongo()
jwt = JWTManager()
images = UploadSet('images', IMAGES)
documents = UploadSet('document', DOCUMENTS)
db = MongoEngine()
redis_client = RedisClient()
mail = Mail()

def create_app(config_name='default'):
    app = Flask(__name__, template_folder= Config.BASE_DIR + os.sep + 'App' + os.sep + 'Templates')
    app.config.from_object(config[config_name])
    db.init_app(app)
    mongod.init_app(app)
    jwt.init_app(app)
    redis_client.init_app(app)
    configure_uploads(app, (images, documents))
    patch_request_class(app) # 16 megabytes
    # 跨域
    CORS(app, supports_credentials=True)
    mail.init_app(app)
    from .iOSApp import iOSApp_api as iOSApp_api_blueprint
    app.register_blueprint(iOSApp_api_blueprint, url_prefix='/iOS')
    return app
