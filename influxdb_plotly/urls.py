# coding: utf-8
from django.conf.urls import url

from . import views

app_name = 'influxdb_plotly'
urlpatterns = [
    # ex: /stream_data/
    url(r'^$', views.stream_data, name='stream_data'),
]
