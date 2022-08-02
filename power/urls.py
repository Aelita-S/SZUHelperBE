from django.urls import include, path
from rest_framework.routers import DefaultRouter

from power.views import PowerViewSet

router = DefaultRouter()
router.register('', PowerViewSet)

urlpatterns = [
    path('power/', include(router.urls)),
]
