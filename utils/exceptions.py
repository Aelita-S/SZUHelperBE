from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError


class WXServiceException(APIException):
    """向微信服务请求时发生错误"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "向微信服务请求时发生错误"


class PowerInquiryException(ValidationError):
    """查询电量信息时，查询参数错误"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "房号错误"


class SysOptionsException(ValidationError):
    """查询系统设置时键不存在"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "查找的键不存在"
