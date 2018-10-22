#!/usr/bin/env python
# coding=utf-8

import logging
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404

from users.serializers import UserSerializer, PasswordSerializer
from users.permissions import IsSuperuserPermission


logger = logging.getLogger(__name__)


class UsersViewSet(GenericViewSet):
    """通过session确定认证，这个viewset下面的api需要session认证通过才能访问"""
    authentication_classes = (SessionAuthentication, )
    # permission_classes = (IsAuthenticated, )

    serializer_class = UserSerializer

    queryset = User.objects

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser, IsSuperuserPermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def list(self, request):
        """users列表
        """
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
        return Response('deleted user: {}'.format(pk),
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        """修改自己的密码

        # TODO(csj): 能不能兼容修改自己和他人的密码
        """
        user = request.user
        serializer = PasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response('invalid data', status=status.HTTP_400_BAD_REQUEST)

        # TODO(csj): 密码没有hash
        serializer.update(user, serializer.validated_data)
        return Response('ok')


class AuthViewSet(GenericViewSet):
    serializer_class = UserSerializer

    queryset = User.objects

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """登录
        ---
        parameters:
          - username
            desc: 用户名
            required: true
            type: string
            in: body
          - password
            desc: 密码
            required: true
            type: string
            in: body
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
            response.set_cookie('csrftoken', value=request.session.get('csrftoken'))  # csrftoken，如果需要的话
            return response
        else:
            return Response('wrong username or password', status=status.HTTP_401_UNAUTHORIZED)

    # 需要用户已经已通过认证
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """注销登录
        """
        logout(request)  # 注销登录，会删除django_session的对应内容

        return Response('ok')
