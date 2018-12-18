#!/usr/bin/env python
# coding=utf-8

from django.urls import re_path

from rest_framework.urlpatterns import include
from rest_framework_nested import routers

from users import views

__all__ = [
    'users_urlpatterns',
    'auth_urlpatterns',
]

app_name = 'users'

auth_router = routers.DefaultRouter()
auth_router.register(r'',
                     views.AuthViewSet,
                     base_name='api-auth')
users_router = routers.DefaultRouter()
users_router.register(r'',
                      views.UsersViewSet,
                      base_name='api-users')

users_urlpatterns = [
    re_path(r'^', include(users_router.urls)),
]
auth_urlpatterns = [
    re_path(r'^', include(auth_router.urls)),
]
