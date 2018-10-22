#!/usr/bin/env python
# coding=utf-8

from rest_framework.permissions import BasePermission


class IsSuperuserPermission(BasePermission):
    """
    请求的用户是否是超级用户
    """
    def has_permission(self, request, view):
        return request.user.is_superuser
