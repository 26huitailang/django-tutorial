#!/usr/bin/env python
# coding=utf-8

from rest_framework import serializers


class FlowPointSerializer(serializers.Serializer):
    time = serializers.DateTimeField(required=True)
    value = serializers.IntegerField(required=True)
    region = serializers.CharField(required=False)
    host = serializers.CharField(required=False)

    class Meta:
        fields = ('time', 'value', 'region', 'host')


class FlowSerializer(serializers.Serializer):
    points = FlowPointSerializer(many=True)
