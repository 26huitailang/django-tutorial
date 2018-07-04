#!/usr/bin/env python
# coding=utf-8

from rest_framework import serializers


class PointsSerializer(serializers.Serializer):
    time = serializers.DateTimeField()


class ListDictSerializer(serializers.ListSerializer):
    points =


