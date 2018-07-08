# coding: utf-8
from django.conf.urls import url

from . import views

app_name = 'mzitu'
urlpatterns = [
    # ex: /mzitu/
    url(r'^$', views.index, name='index'),
    url(r'^download_one_suit$', views.parse_and_download_one_suit, name='download_one_suit'),
    url(r'^download_one_theme$', views.download_one_theme, name='download_one_theme'),
    url(r'^get_proxies$', views.get_proxies, name='get_proxies'),
    url(r'^async_parse_and_download_one_suit$', views.async_parse_and_download_one_suit, name='async_parse_and_download_one_suit')
]
