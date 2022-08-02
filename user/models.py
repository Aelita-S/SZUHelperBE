from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.base_models import JSONSchemaField

# 设置项校验，如果需要添加设置字段，需要同时在schema中添加字段
config_schema = {
    "type": "object",
    "properties": {
        "dormitory": {
            "type": "object",
            "description": "宿舍",
            "properties": {
                "subscribe": {"type": "boolean", "description": "是否订阅"},
                "campusName": {"type": "string", "description": "校区名"},
                "areaName": {"type": "string", "description": "宿舍区域名"},  #
                "buildingName": {"type": "string", "description": "宿舍楼名"},
                "buildingID": {"type": "number", "description": "宿舍楼栋id（szu_id）"},
                "roomNo": {"type": "number", "description": "房间号"},
            },
            "if": {"properties": {"subscribe": {"const": True}}},  # 条件校验，只有订阅了才需要填写其他信息
            "then": {"required": ["subscribe", "campusName", "areaName", "buildingName", "buildingID", "roomNo"]},
            "else": {"required": ["subscribe"]}
        }
    },
    "required": ["dormitory"],  # 主设置项
}


def default_config():
    config = {
        "dormitory": {
            "subscribe": False,
            "campusName": "",
            "areaName": "",
            "buildingName": "",
            "buildingID": -1,
            "roomNo": -1,
        }
    }
    return config


class User(AbstractUser):
    username = models.CharField(verbose_name='openid', primary_key=True, max_length=50, unique=True,
                                error_messages={
                                    'unique': "A user with that openid already exists.",
                                }, help_text="微信用户唯一标识openid，作为主键")
    config = JSONSchemaField(help_text="用户设置", default=default_config, schema=config_schema)

    # @property
    # def power_subscribed_users(self):
    #     """返回电量订阅用户"""
    #     return User.objects.filter(config__dormitory__subscribe=True)
