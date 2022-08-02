from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.models import User
from user.serializers import UserLoginSerializer


class UserLoginViewSet(GenericViewSet):
    """小程序发送"""
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @action(methods=('POST',), detail=False)
    def login(self, request, *args, **kwargs):
        pass


class UserInfoViewSet(GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    @action(methods=('get', 'put'), detail=False)
    def config(self, request, *args, **kwargs):
        openid = request.user
        user = self.get_queryset().get(username=openid)
        method = request.method.lower()
        if method == 'get':
            data = user.config
            return Response(data)
        elif method == 'put':
            user.config = request.data
            user.save()
            return Response(user.config)
