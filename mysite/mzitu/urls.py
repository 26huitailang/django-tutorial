# coding: utf-8
from django.conf.urls import url
from django.urls import re_path, path

from rest_framework.urlpatterns import include
from rest_framework_nested import routers

from . import views

__all__ = [
    'urlpatterns',
    # 'suite_urlpatterns',
    # 'theme_urlpatterns',
]

app_name = 'mzitu'

suite_router = routers.DefaultRouter()
suite_router.register(
    r'',
    views.suite.MzituSuiteViewSet,
    base_name='api-mzitu-suite'
)
theme_router = routers.DefaultRouter()
theme_router.register(
    r'',
    views.theme.MzituThemeViewSet,
    base_name='api-mzitu-theme',
)
proxyip_router = routers.DefaultRouter()
proxyip_router.register(
    r'',
    views.proxy_ip.ProxyIpViewSet,
    base_name='api-mzitu-proxyip',
)
tag_router = routers.DefaultRouter()
tag_router.register(
    r'',
    views.tag.TagViewSet,
    base_name='api-mzitu-tag',
)

suite_urlpatterns = [
    re_path(r'^', include(suite_router.urls)),
]
theme_urlpatterns = [
    re_path(r'^', include(theme_router.urls)),
]
proxyip_urlpatterns = [
    re_path(r'^', include(proxyip_router.urls)),
]

urlpatterns = [
    # ex: /mzitu/
    path('suites/', include(suite_urlpatterns)),
    path('themes/', include(theme_urlpatterns)),
    path('proxyips/', include(proxyip_urlpatterns)),
    re_path(r'tags/', include(tag_router.urls)),
]
