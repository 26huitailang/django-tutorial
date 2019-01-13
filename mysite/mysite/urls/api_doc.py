#!/usr/bin/env python
# coding=utf-8


from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


__all__ = ['urlpatterns']

schema_view = get_schema_view(
    openapi.Info(
        title="Mysite API",
        default_version='v1',
        description="Test description",
        contact=openapi.Contact(email="26huitailang@gmail.com"),
        license=openapi.License(name="Commercial License"),
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]
