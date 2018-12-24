#!/usr/bin/env python
# coding: utf-8

from rest_framework import serializers
from mzitu.models.downloaded_suite import DownloadedSuite, SuiteImageMap
from mzitu.models.tag import Tag


class SuiteImageMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuiteImageMap
        fields = '__all__'


class TagSerailizer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class MzituDownloadedSuiteSerializer(serializers.ModelSerializer):
    images = SuiteImageMapSerializer(many=True, read_only=True)
    tags = TagSerailizer(many=True, read_only=True)  # todo: serailizer.SerializerMethodField

    class Meta:
        model = DownloadedSuite
        fields = ('id', 'name', 'url', 'max_page', 'tags', 'images')


