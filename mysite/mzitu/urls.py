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

suit_router = routers.DefaultRouter()
suit_router.register(
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

suite_urlpatterns = [
    re_path(r'^', include(suit_router.urls)),
]
theme_urlpatterns = [
    re_path(r'^', include(theme_router.urls)),
]
proxyip_urlpatterns = [
    re_path(r'^', include(proxyip_router.urls)),
]

urlpatterns = [
    # ex: /mzitu/
    url(r'^$', views.suite.index, name='index'),
    path('suite/', include(suite_urlpatterns)),
    path('theme/', include(theme_urlpatterns)),
    path('proxyip/', include(proxyip_urlpatterns)),
]
