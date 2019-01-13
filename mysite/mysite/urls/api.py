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
from users.urls import users_urlpatterns, auth_urlpatterns
from mzitu.urls import urlpatterns as mzitu_urlpatterns


# api base v1
v1_urlpatterns = [
    url(r'polls/', include('polls.urls')),
    url(r'mzitu/', include(mzitu_urlpatterns)),
    url(r'influxdb_plotly/', include('influxdb_plotly.urls')),
    url(r'users/', include(users_urlpatterns)),
    url(r'auth/', include(auth_urlpatterns)),
]

# todo: version test
v2_urlpatterns = [
    url(r'users/', include(users_urlpatterns))
]
