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
from django.views.static import serve
from django.urls import include, path
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
from mysite.deploy_level import DeployLevel
from users.views.auth_token import CustomAuthToken
# from rest_framework.authtoken import views

from .api import v1_urlpatterns as v1_api_urlpatterns
from .api import v2_urlpatterns as v2_api_urlpatterns

urlpatterns = [
    # api versioning，在view中做版本的管理，在这里路由到不同的views下面
    # [参考](https://gearheart.io/blog/api-versioning-with-django-rest-framework/)
    # path('api/v1/', include((api_urls, 'v1'), namespace='v1')),
    # path('api/v2/', include((api_urls, 'v2'), namespace='v2')),
    path('', TemplateView.as_view(template_name="index.html")),
    # url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api-token-auth/', CustomAuthToken.as_view()),
]

if settings.DEPLOY_LEVEL <= DeployLevel.develop:
    # for admin
    urlpatterns += [
        path('admin/', admin.site.urls),
        # 根据MEDIA_ROOT结合url来访问文件
        url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    ]

    # for swagger
    # swagger version control, in separate page
    from . import api_doc
    v1_api_urlpatterns += api_doc.urlpatterns
    v2_api_urlpatterns += api_doc.urlpatterns

# todo: include app_name problem，精确到viewset的版本控制
urlpatterns += [
    path('api/v1/', include((v1_api_urlpatterns, 'v1'), namespace='v1')),
    path('api/v2/', include((v2_api_urlpatterns, 'v2'), namespace='v2')),
]
