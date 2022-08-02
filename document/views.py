from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from document.models import Document
from document.serializers import DocumentListSerializer, DocumentSerializer


class DocumentReadViewSet(ReadOnlyModelViewSet):
    queryset = Document.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('department', 'category')

    @method_decorator(cache_page(24 * 3600))  # 具体文章缓存一天
    def retrieve(self, request, *args, **kwargs):
        return super(DocumentReadViewSet, self).retrieve(self, request, *args, **kwargs)

    @method_decorator(cache_page(5 * 60))  # 文章列表缓存5分钟
    def list(self, request, *args, **kwargs):
        return super(DocumentReadViewSet, self).list(self, request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentListSerializer
        elif self.action == 'retrieve':
            return DocumentSerializer
