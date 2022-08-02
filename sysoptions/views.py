from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from utils.cache import SysOptionsCache, ViewsCache


@api_view(('GET',))
def ping(request: Request):
    return Response({'views': ViewsCache.get()})


@api_view(('GET',))
def view(request: Request):
    return Response({'views': ViewsCache.incr()})


@api_view(('GET',))
def get_options(request: Request, key: str):
    return Response(SysOptionsCache.get(key))
