#!/usr/bin/env python
# coding: utf-8

from rest_framework import serializers
from mzitu.models.downloaded_suit import DownloadedSuit


class MzituDownloadedSuitSerializer(serializers.ModelSerializer):

    class Meta:
        model = DownloadedSuit
        fields = '__all__'