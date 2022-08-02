from django.urls import path

from sysoptions.views import get_options, ping, view

urlpatterns = [
    path('ping/', ping),
    path('view/', view),
    path('sys/options/<str:key>', get_options)
]
