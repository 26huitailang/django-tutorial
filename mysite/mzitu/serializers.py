#!/usr/bin/env python
# coding: utf-8

from rest_framework import serializers
from mzitu.models.downloaded_suite import DownloadedSuite, SuiteImageMap


class SuiteImageMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuiteImageMap
        fields = '__all__'


class MzituDownloadedSuiteSerializer(serializers.ModelSerializer):
    images = SuiteImageMapSerializer(many=True, read_only=True)

    class Meta:
        model = DownloadedSuite
        fields = ('id', 'name', 'url', 'max_page', 'tag', 'images')
