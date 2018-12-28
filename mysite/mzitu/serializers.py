#!/usr/bin/env python
# coding: utf-8

from rest_framework import serializers
from mzitu.models.downloaded_suite import DownloadedSuite, SuiteImageMap
from mzitu.models.tag import Tag


class SuiteImageMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuiteImageMap
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    suites_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = '__all__'

    def get_suites_count(self, obj):
        count = obj.downloadedsuite_set.count()
        return count


class MzituDownloadedSuiteSerializer(serializers.ModelSerializer):
    images = SuiteImageMapSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)  # todo: serailizer.SerializerMethodField
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = DownloadedSuite
        # fields = ('id', 'name', 'url', 'max_page', 'tags', 'images')
        fields = '__all__'
