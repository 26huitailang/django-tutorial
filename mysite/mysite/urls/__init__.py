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
from django.urls import include, path
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
from mysite.deploy_level import DeployLevel

from . import api as api_urls


urlpatterns = [
    # api versioning，在view中做版本的管理，在这里路由到不同的views下面
    # [参考](https://gearheart.io/blog/api-versioning-with-django-rest-framework/)
    path('api/', include(api_urls)),
    path('', TemplateView.as_view(template_name="index.html")),
]


if settings.DEPLOY_LEVEL <= DeployLevel.develop:
    # for admin
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]

    # for swagger
    from . import api_doc
    urlpatterns += api_doc.urlpatterns
