from flask import Blueprint

iOSApp_api = Blueprint('iOSApp', __name__)

from App.iOSApp import Route


