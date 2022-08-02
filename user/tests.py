from rest_framework.test import APITestCase

from user.models import User


class UserLoginTestCase(APITestCase):
    def setUp(self) -> None:
        User.objects.create(openid='123456')
        # TODO 完善单元测试
