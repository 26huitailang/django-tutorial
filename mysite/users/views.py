#!/usr/bin/env python
# coding=utf-8

import logging
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from users.serializers import UserSerializer


logger = logging.getLogger(__name__)


class UsersViewSet(GenericViewSet):
    """通过session确定认证，这个viewset下面的api需要session认证通过才能访问"""
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    serializer_class = UserSerializer

    queryset = User.objects

    def list(self, request):
        """users list
        """
        users = self.queryset.values('id', 'username', 'is_superuser')
        return Response({'data': users})


class AuthViewSet(GenericViewSet):
    serializer_class = UserSerializer

    queryset = User.objects

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """login
        """
        # username = request.POST.get('username', None)
        # password = request.POST.get('password', None)
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None or password is None:
            return Response('no username or password', status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = Response('ok')
            response.set_cookie('sessionid', value=request.session.get('sessionid'))  # 设置浏览器需要的cookie
            # response.set_cookie('csrftoken', value=request.session.get('csrftoken'))  # csrftoken，如果需要的话
            return response
        else:
            return Response('wrong username or password', status=status.HTTP_401_UNAUTHORIZED)

    # 需要用户已经已通过认证
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)  # 注销登录，会删除django_session的对应内容

        return Response('ok')
