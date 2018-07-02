# coding: utf-8
from django.conf.urls import url

from . import views

app_name = 'influxdb_plotly'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /stream_data/
    url(r'^stream_data/$', views.stream_data, name='stream_data'),
]
