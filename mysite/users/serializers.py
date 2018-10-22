#!/usr/bin/env python
# coding=utf-8

from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser', )


class PasswordSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField()

    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance
