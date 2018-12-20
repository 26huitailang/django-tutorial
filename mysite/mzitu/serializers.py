#!/usr/bin/env python
# coding: utf-8

from rest_framework import serializers
from mzitu.models.downloaded_suite import DownloadedSuite


class MzituDownloadedSuiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = DownloadedSuite
        fields = '__all__'
