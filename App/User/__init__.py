from flask import Blueprint

user_api = Blueprint('user', __name__)

dealer_user_api = Blueprint('dealer_user', __name__)

admin_user_api = Blueprint('admin_user_api', __name__)

from App.User import Route

from App import redis_client

