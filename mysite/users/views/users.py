#!/usr/bin/env python
# coding=utf-8

import logging
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema

from users.serializers import (
    UserSerializer,
    PasswordSerializer,
    LoginSerializer,
)
from users.permissions import IsSuperuserPermission


logger = logging.getLogger(__name__)


class UsersViewSet(GenericViewSet):
    """通过session确定认证，这个viewset下面的api需要session认证通过才能访问"""
    # authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAdminUser,)
    # versioning_class = URLPathVersioning
    serializer_class = UserSerializer
    queryset = User.objects

    # def get_permissios(self, request):
    #     """按不同action返回权限类"""
    #     self.action
    #     request.method
    #     pass

    def retrieve(self, request, pk=None):
        """指定用户信息
        """
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    # @permission_classes((IsAdminUser, ))
    def list(self, request):
        """users列表
        """
        print(request.version)
        users = self.queryset.values('id', 'username', 'is_staff')
        return Response({'data': users})

    def create(self, request):
        """创建用户
        """
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            return Response('no username or password', status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        if user:
            return Response('duplicated username', status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            password=password,
            # is_superuser=False,
            # is_staff=False,
        )
        user.save()
        return Response('ok', status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """删除用户
        """
        user = get_object_or_404(self.queryset, pk=pk)
        user.delete()
        return Response('deleted user: {}'.format(pk))

    @action(detail=True, methods=['POST'])
    def change_password(self, request, pk=None):
        """修改指定user id的密码
        ---
        parameters:
          - pk
            desc: 用户id
            required: true
            type: string
            in: path
        """
        user = get_object_or_404(self.queryset, pk=pk)

        # 如果修改他人密码需要superuser
        if user.id != request.user.id and request.user.is_superuser is False:
            return Response('not superuser', status=status.HTTP_403_FORBIDDEN)

        serializer = PasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response('invalid data', status=status.HTTP_400_BAD_REQUEST)

        serializer.update(user, serializer.validated_data)
        return Response('ok')


class AuthViewSet(GenericViewSet):
    serializer_class = LoginSerializer

    queryset = User.objects

    @swagger_auto_schema(deprecated=True)
    @action(detail=False, methods=['POST'], permission_classes=[])  # 覆盖全局设置，避免IsAuthenticated限制login
    def login(self, request):
        """登录
        ---
        parameters:
          - name: username
            desc: 用户名
            required: true
            type: string
            in: body
          - name: password
            desc: 密码
            required: true
            type: string
            in: body
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response('no username or password', status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request,
                            username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])
        if user is not None:
            login(request, user)
            response = Response('ok')
            response.set_cookie('sessionid', value=request.session.get('sessionid'))  # 设置浏览器需要的cookie
            response.set_cookie('csrftoken', value=request.session.get('csrftoken'))  # csrftoken，如果需要的话
            return response
        else:
            return Response('invalid username or password', status=status.HTTP_400_BAD_REQUEST)

    # 需要用户已经已通过认证
    @swagger_auto_schema(deprecated=True)
    @action(detail=False, methods=['GET'])
    def logout(self, request):
        """注销登录
        """
        logout(request)  # 注销登录，会删除django_session的对应内容

        return Response('ok')
