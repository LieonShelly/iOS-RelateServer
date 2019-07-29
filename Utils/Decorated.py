from functools import wraps
import re
from Utils.ResultHandle import fail
from Utils.Tools import is_number
from flask import abort, request
from App import redis_client
import json
from .DateTimeTool import return_time_now


def phone_number_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        regex = re.compile(
            '^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$'
        )
        if "phone_num" not in request.json:
            return fail(message="phone_num 为空", code=20001)
        phone_num = str(request.json.get('phone_num'))
        if regex.search(phone_num) == None:
            return fail(message="Phone Number Error", code=20001)
        return f(*args, **kwargs)

    return decorated_function


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            current_user_str = redis_client.get(token)
            if token is None or current_user_str is None:
                return fail(message="没有权限", code=20003)
            current_user = json.loads(current_user_str)
            from App.User.Model import PositionType
            # 经理默认所有权限
            if current_user['position'] is PositionType.manager:
                return f(*args, **kwargs)
            permissions = current_user['permissions']
            if permissions is None:
                return fail(message="没有权限", code=20003)
            if permission not in permissions:
                return fail(message="没有权限", code=20003)
            return f(*args, **kwargs)

        return decorated_function

    return decorator



# 验证请求参数是否未空
def valid_none_params(*keys):
    def decorator(f):
        @wraps(f)
        def validFn(*args, **kwargs):
            method = request.method
            recv = request.args if method == 'GET' else request.json or request.form 
            for item in keys:
                if recv.get(item) is None:
                    # return f({'valid': False})
                    return fail(message='缺少参数' + item)

            # recv['valid'] = True
            return f()

        return validFn

    return decorator

def valid_form_params(*keys):
    def decorator(f):
        @wraps(f)
        def validFn(*args, **kwargs):
            method = request.method
            recv = request.form 
            for item in keys:
                if recv.get(item) is None:
                    # return f({'valid': False})
                    return fail(message='缺少参数' + item)

            # recv['valid'] = True
            return f()

        return validFn

    return decorator


# 验证get请求的分页参数
def pagination_required(func):
    @wraps(func)
    def validFn(*args, **kwargs):  # 处理传入函数的参数
        recv = request.args
        page = recv.get('page')
        page_length = recv.get('page_length')
        if not page or not page_length:
            return fail(message='缺少分页参数')
        elif not is_number(page):
            return fail(message='页码数据异常')
        elif not is_number(page_length):
            return fail(message='页长数据异常')
        else:
            return func(*args, **kwargs)

    return validFn


# 请求参数校验器
def params_validator(*keys):
    def decorator(f):
        @wraps(f)
        def validFn(*args, **kwargs):
            method = request.method
            recv = request.args if method == 'GET' else request.json or {}
            for item in keys:
                # 如果参数不为数组形式
                if not isinstance(item, list):
                    el = recv.get(item)
                    if el is None:
                        return fail(message='缺少参数' + item)
                else:
                    el = recv.get(item[0])
                    # 请求参数中不包含需要的参数
                    if el is None:
                        return fail(message='缺少参数' + item[0])
                    if not isinstance(el, item[1]):
                        return fail(message='参数' + item[0] + '类型错误')
            return f()

        return validFn

    return decorator


def company_in_use_time_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = user_actions.current_user()
        if user is None:
            return fail(message="company_in_use_time_required-没有登录")
        company = user.get('company')
        if company is None:
            return fail(message="使用时间到期，请联系平台处理-1", code=20010)
        compay_id = company.get("$oid")
        expire_time = compamy_use_time(compay_id)
        if expire_time < return_time_now() or expire_time is None:
            return fail(message="使用时间到期，请联系平台处理-2", code=20010)
        return f(*args, **kwargs)
    return decorated_function




def dealer_company_in_use_time_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from App.Company.Actions import current_cache_dealer_company
        from App.Token.Actions import get_jwt_identity
        admin_account = get_jwt_identity()
        redis_company = current_cache_dealer_company(account=admin_account)
        vip_expired = redis_company.get('vip_expired')
        if admin_account is None:
            return fail(message="dealer_company_in_use_time_required-没有登录")
        if vip_expired is None:
            return fail(message="使用时间到期，请联系平台处理", code=20010)
        expire_time = vip_expired
        if expire_time < return_time_now():
            return fail(message="使用时间到期，请联系平台处理return_time_now", code=20010)
        return f(*args, **kwargs)
    return decorated_function
