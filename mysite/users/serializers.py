#!/usr/bin/env python
# coding=utf-8

from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser', 'is_staff', 'last_login', )


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

    def update(self, instance, validated_data):
        password = validated_data.get('password', instance.password)
        instance.set_password(password)  # hash password
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
