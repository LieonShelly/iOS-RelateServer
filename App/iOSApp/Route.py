from . import iOSApp_api
from flask import request
from Utils import Decorated as decorated
from Utils import ResultHandle as result_handle
import random
from App.iOSApp import Actions as action

@iOSApp_api.route('/send_code', methods = ['POST'])
@decorated.params_validator(
    ['to_email', str]
)
def send_code():
    result = action.send_verifycode(request.json)
    return result_handle.response(result)


@iOSApp_api.route('/send_message', methods = ['POST'])
@decorated.params_validator(
    ['title', str],
    ['content', str],
    ['to_email', str]
)
def send_message():
    result = action.send_mssage(request.json)
    return result_handle.response(result)