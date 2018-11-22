"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from users.urls import users_urlpatterns
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Django Tutorial API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^apidocs/$', schema_view),
    url(r'^polls/', include('polls.urls')),
    url(r'^mzitu/', include('mzitu.urls')),
    url(r'^influxdb_plotly/', include('influxdb_plotly.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^', include(users_urlpatterns)),
]
