from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views import UserInfoViewSet, UserLoginViewSet

router = DefaultRouter()

router.register('', UserLoginViewSet)
router.register('', UserInfoViewSet)

urlpatterns = [
    path('user/', include(router.urls))
]
