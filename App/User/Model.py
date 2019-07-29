from App import db
from App.Position.Model import PositionType
from App.UserPermission.Model import UserPermission
from datetime import datetime
from App.Company.Model import Company
from App.Base.Model import BaseDocument, DocumentStatus
from App.UserPermission.Model import Permission
from Utils.Tools import random_str
import json

# class TestUser(BaseDocument, db.Document):
    
#     meta = {"db_alias": "test-db"}


class GendarType:
    male = 1
    female = 2
    unknown = 3

    @classmethod
    def title(cls, value):
        if value == 1:
            return "男"
        elif value == 2:
            return "女"
        return ""


class User(BaseDocument, db.Document):
    head_img = db.StringField()
    name = db.StringField(default=random_str)
    phone_num = db.StringField(required=True)
    position = db.IntField(choices=(PositionType.manager, 
                                PositionType.salesman, 
                                PositionType.undefine),
                            default=PositionType.undefine)
    gendar = db.IntField(
        choices=(GendarType.male, GendarType.female,
                 GendarType.unknown), required=True, default=GendarType.unknown)  # 1 男 2 女 3.未设置
    birthday = db.StringField()
    permissions = db.ListField(
        db.IntField(
            choices=(Permission.factory_finacial,
                     Permission.news_dealer_welfare,
                     Permission.company_4s_manager,
                     Permission.news_manage_class, Permission.news_sale_class,
                     Permission.distribute_post,
                     Permission.review_defeat_apply)))
    company = db.ReferenceField(Company)
    registration_id = db.StringField()
    device_id = db.StringField()

    @db.queryset_manager
    def salesman_objects(doc_cls, queryset):
        return queryset.filter(status=DocumentStatus.NORMAL, position = PositionType.salesman).order_by('-create_time')

    @db.queryset_manager
    def objects(doc_cls, queryset):
        return queryset.filter(status=DocumentStatus.NORMAL).order_by('-create_time')
    
    def to_dict_reponse(self):
        db_user_json = json.loads(self.to_json())
        db_user_json["user_name"] = self.name
        db_user_json["user_id"] = str(self.id)
        db_user_json["company_full_name"] = self.company.company_full_name if self.company else ""
        db_user_json["company_id"] = str(self.company.id) if self.company else ""
        db_user_json["company_status"] = self.company.verify_status if self.company else "3"
        db_user_json["company_vip_expired"] = self.company.vip_expired if self.company else "0"
        db_user_json["company_info"] = self.company.to_dict_reponse() if self.company else {}
        from App.SystemConfig.Model import SystemParameter, SystemParameterCodeType
        import re
        reg = re.compile('<[^>]*>')
        service_phone = SystemParameter.objects(code_type = SystemParameterCodeType.CONTACT_US).first()
        db_user_json["service_phone"] = reg.sub('', service_phone.content).replace('\n','').replace(' ','') if service_phone else ""
        return db_user_json



class Comment(db.EmbeddedDocument):
    content = db.StringField()


class Page(db.Document):
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    author = db.ReferenceField(User)