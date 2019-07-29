from App.User import user_api, dealer_user_api, admin_user_api
from Utils import ResultHandle
from flask import request
from App.User import Actions
from App.Token import Actions as TokenAction
from Utils import Decorated as decorated
from App.Company import Actions as company_actions
import json
from App import logger

@user_api.before_request
@TokenAction.jwt_required
def before_request():
    pass

@dealer_user_api.before_request
@TokenAction.jwt_required
@decorated.dealer_company_in_use_time_required
def before_request():
    pass

# @user_api.route('/test/add'):
#     from .Model import TestUser
#     user = TestUser()
#     user.save()
#     result = TestUser.objects()
#     return ResultHandle.success(data= {"data": json.loads(result.to_json())})

# 添加员工
@user_api.route("/add", methods=['post'])
@TokenAction.jwt_required
@decorated.company_in_use_time_required
@decorated.params_validator(
    ["head_img", str],
    # ["name", str],
    ["phone_num", str],
    ["position", int],
    ["gendar", int],
    ["birthday", str],
    ["permissions", list],
    ["company", str]
)
def add():
    recvdata = request.json
    result = Actions.add(recvdata)
    return ResultHandle.response(result)

# 删除用户
@user_api.route("/delete", methods=['post'])
@TokenAction.jwt_required
@decorated.company_in_use_time_required
@decorated.params_validator(
    ["user_id", str]
)
@decorated.manager_required
def delete_user():
    user_id = request.json.get('user_id')
    result = Actions.remove_user(user_id)
    return ResultHandle.response(result)

# 员工列表
@user_api.route("/lists", methods=['GET'])
@TokenAction.jwt_required
@decorated.company_in_use_time_required
@decorated.manager_required
def user_lists():
    page = request.args.get('page') or 1
    per_page = request.args.get('per_page') or 20
    is_filter_self = request.args.get('is_filter_self') or 0
    is_filter_self = int(is_filter_self)
    filter_users = []
    if is_filter_self == 1:
        filter_users = [Actions.current_user_id()]
    company_id = company_actions.current_company_id()
    result = Actions.user_lists(query = {"company": company_id}, filter_users=filter_users, page=int(page), per_page=int(per_page))
    return ResultHandle.response(result)


# 用户详情 - APP
@user_api.route("/detail", methods=['GET'])
def get():
    try:
        if "user_id" in request.args:
            user_id = request.args.get('user_id')
            info = Actions.user_info({"id": user_id})
        else:
            info = Actions.current_user()
    except Exception as e:
        from App import logger
        logger.exception(e)
        return ResultHandle.fail()
    return ResultHandle.success(data={"info": info})

# 编辑员工 - APP
@user_api.route('/update', methods=['post'])
@decorated.params_validator(
    ["user_id", str]
)
def update():
    update_body = request.json
    user_id = update_body.pop('user_id')
    result = Actions.update_user(user_id=user_id, update_body=update_body)
    return ResultHandle.response(result)


#  员工列表 - 经销商
@dealer_user_api.route("/lists",  methods=['get'])
def dealer_user_lists():
    page = int(request.args.get('page')) or 1
    per_page = int(request.args.get('per_page')) or 1
    account = TokenAction.get_jwt_identity()
    company_id = company_actions.current_cache_dealer_company(account=account).get('company_id')
    result = Actions.user_lists(page=int(page), per_page=int(per_page), query =  {"company": company_id})
    return ResultHandle.response(result)



# 编辑员工
@dealer_user_api.route('/update', methods=['post'])
@decorated.params_validator(
    ["user_id", str]
)
def update():
    update_body = request.json
    user_id = update_body.pop('user_id')
    result = Actions.update_user(user_id=user_id, update_body=update_body)
    return ResultHandle.response(result)


@dealer_user_api.route("/delete", methods=['post'])
@decorated.params_validator(
    ["user_id", str]
)
def delete_user():
    user_id = request.json.get('user_id')
    result = Actions.remove_user(user_id)
    return ResultHandle.response(result)



@admin_user_api.route("/delete", methods=['POST'])
@decorated.params_validator(
    ["user_id", str]
)
def delete_user():
    user_id = request.json.get('user_id')
    result = Actions.remove_user(user_id)
    return ResultHandle.response(result)



@admin_user_api.route("/lists", methods=['GET'])
@TokenAction.jwt_required
def user_lists():
    page = int(request.args.get('page') or 1) 
    per_page = int(request.args.get('per_page') or 20)
    query = {}
    if "name" in request.args:
        query["name"] = request.args.get('name')
    if "phone_num" in request.args:
        query["phone_num"] = request.args.get('phone_num')
    result = Actions.user_lists(page=int(page), per_page=int(per_page), query = query)
    return ResultHandle.response(result)



@admin_user_api.route("/init_all_own", methods=['GET'])
@TokenAction.jwt_required
def init_all_own():
    from App.PerformanceStatistic.Actions import init_data
    from .Model import User
    lists = User.objects()
    for user in lists:
        init_data(user)
    return ResultHandle.success()