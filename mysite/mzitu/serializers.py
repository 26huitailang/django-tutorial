#!/usr/bin/env python
# coding: utf-8

from rest_framework import serializers

from mzitu.models.downloaded_suite import DownloadedSuite, SuiteImageMap
from mzitu.models.tag import Tag
from mzitu.runtimes.suite import get_local_suite_count


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
    images = SuiteImageMapSerializer(many=True, read_only=True)  # 数据库对象
    tags = TagSerializer(many=True, read_only=True)  # todo: serailizer.SerializerMethodField
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    locals_count = serializers.SerializerMethodField()  # 本地文件数量

    class Meta:
        model = DownloadedSuite
        # fields = ('id', 'name', 'url', 'max_page', 'tags', 'images')
        fields = '__all__'

    def get_locals_count(self, obj):
        return get_local_suite_count(obj.name)
