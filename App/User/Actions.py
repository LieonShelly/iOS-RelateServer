from .Model import User, PositionType
from App.Position.Model import Position as PositionModel
from App.UserPermission.Model import UserPermission as UserPermissionModel
from App.Company.Model import Company as CompanyModel
from App.Company import Actions as company_actions
from App import redis_client
from flask import request
import json
from flask_jwt_extended import get_jwt_identity
from Config import RedisDBConfig
from App import logger
from Utils import DateTimeTool as time_tool


# 添加用户
def add(userinfo):
    phone_num = userinfo["phone_num"]
    company = userinfo.pop('company')
    exist_user_count = User.objects(phone_num=phone_num, company=company).count()
    if exist_user_count > 0:
        return (False, "销售已经存在该公司")
    exist_user_count = User.objects(phone_num=phone_num, company__nin = [company], position__nin = [PositionType.undefine]).count() # 该销售在其他公司存在
    if exist_user_count > 0:
        return (False, "销售已经存在其他公司，请联系万车宝客服")
    belong_company = CompanyModel.objects(id=str(company)).first()
    result = User.objects(phone_num=phone_num).update(**userinfo, company=belong_company, upsert=True)
    document =  User.objects(phone_num=phone_num).first()
    from App.PerformanceStatistic import Actions as statisticAction
    statisticAction.init_data(document)
    return (True, {})

# 删除用户
def remove_user(user_id):
    try:
        from App.Base.Model import DocumentStatus
        from App.Client.Model import Client,ClientTackingStatus
        client_count = Client.objects(salesman=user_id, tracking_status=ClientTackingStatus.tracking).count()
        if client_count > 0:
            return (False, "该销售有跟进中的意向客户，是否现在转移")
        User.objects(id=user_id).update(status=DocumentStatus.DELETEED)
    except Exception as e:
        logger.exception(e)
        return (False, "操作异常")
    return (True, {})

# 更新用户信息
def update_user(user_id, update_body):
    try:
        token_json = {}
        if "company" in update_body:
            company = update_body.pop('company')
            from bson import ObjectId
            company_id = ObjectId(oid=company)
            User.objects(id=user_id).update(company=company_id)
        
        if "phone_num" in  update_body: # 如果电话号码更新了，则先退出
            phone_num = update_body.get('phone_num')
            pre_phone_num = User.objects(id=user_id).first().phone_num
            if phone_num != pre_phone_num: 
                if User.objects(phone_num = phone_num).count() > 0:
                    return False, "此电话号码已存在"
                redis_client.delete(RedisDBConfig.sso_key + pre_phone_num)
                from App.Token.Actions import create_token
                token_json = create_token(phone_num)
        result = User.objects(id=user_id).update(**update_body)
        db_user = User.objects(id=user_id).first()
        cache_user(phone_num=db_user.phone_num, user_str=json.dumps(db_user.to_dict_reponse())) 
        response = { "user_info":db_user.to_dict_reponse() }
        if len(token_json.keys()) > 0:
            response["token_data"] = token_json
        return True, response
            
        
    except Exception as e:
        logger.exception(e)
        return (False, "操作异常")


# 员工列表
def user_lists(query, filter_users=[], page=1, per_page=20):
    try:
        skip_index = (page -1) * per_page
        lists = User.objects(**query, id__nin=filter_users).skip(skip_index).limit(per_page)
        user_lists = []
        for user in lists:
            user_lists.append(user.to_dict_reponse())
    except Exception as e:
        logger.exception(e)
        return (False, "操作异常")
    return (True, {"lists": user_lists, "total_count":User.objects(**query, id__nin=filter_users).count()})



# 缓存用户信息
def cache_user(phone_num, user_str):
    key = RedisDBConfig.user_info + phone_num
    redis_client.set(key, user_str)


# 在缓存中获取当前的用户
def current_user():
    phone_num = get_jwt_identity()
    if phone_num is None:
        return None
    key = RedisDBConfig.user_info + phone_num
    current_user_str = redis_client.get(key)
    if current_user_str is None:
        from App.User import Model as UserModel
        db_user=UserModel.User.objects(phone_num=phone_num).first()
        user_str = db_user.to_dict_reponse()
        cache_user(phone_num, user_str)
        return json.loads(user_str)
    current_user = json.loads(current_user_str)
    return current_user


def current_user_id():
    user = current_user()
    user_id = user.get("_id").get("$oid")
    return user_id

def user_info(query):
    try:
        db_user = User.objects(**query).first()
        db_user_json = db_user.to_dict_reponse()
        return db_user_json
    except Exception as e:
        logger.exception("USER INFO ERROR:", e)
        return {}
   

def permission_required(permission):
    current_user = current_user()
    from App.User.Model import PositionType
    # 经理默认所有权限
    if current_user['position'] is PositionType.manager:
        return True
    permissions = current_user['permissions']
    if permissions is None:
        return False
    if permission not in permissions:
        return False
    return True

def user_permission_required(user_json, permission):
    current_user = user_json
    from App.User.Model import PositionType
    # 经理默认所有权限
    if current_user['position'] is PositionType.manager:
        return True
    permissions = current_user['permissions']
    if permissions is None:
        return False
    if permission not in permissions:
        return False
    return True