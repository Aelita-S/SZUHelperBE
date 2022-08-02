import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()
logger = logging.getLogger(__name__)


class CustomBackend(ModelBackend):
    """
    自定义用户认证(openid登录)
    自定义用户认证时，需要把这个认证类放到 settings.py 中的 AUTHENTICATION_BACKENDS 中
    """

    def authenticate(self, request, username=None, **kwargs):
        """因使用微信官方认证，所以跳过自行认证，直接在数据库中获取用户

        :param request:
        :param username: 即openid
        :param kwargs:
        :return:
        """
        try:
            user = User.objects.get(username=username)
            return user
        except Exception as e:
            logger.error(repr(e))
            return None
