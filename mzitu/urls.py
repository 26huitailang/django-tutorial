# coding: utf-8
from django.conf.urls import url

from . import views

app_name = 'mzitu'
urlpatterns = [
    # ex: /mzitu/
    url(r'^$', views.index, name='index'),
    url(r'^download_one_suit$', views.download_one_suit, name='download_one_suit'),
    url(r'^get_proxies$', views.get_proxies, name='get_proxies'),
]
