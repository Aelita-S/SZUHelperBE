from django.urls import include, path
from rest_framework.routers import DefaultRouter

from document.views import DocumentReadViewSet

router = DefaultRouter()
router.register('', DocumentReadViewSet)

urlpatterns = [
    path('documents/', include(router.urls)),
]
