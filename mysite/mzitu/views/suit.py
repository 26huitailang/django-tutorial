# coding: utf-8

import random
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from mzitu.constants import (
    USER_AGENT_LIST,
)
from mzitu.models.downloaded_suit import DownloadedSuit
from mzitu.serializers import MzituDownloadedSuitSerializer
from mzitu.tasks.suit import download_one_suit


class MzituSuitViewSet(GenericViewSet):
    serializer_class = MzituDownloadedSuitSerializer
    queryset = DownloadedSuit.objects.all()

    @swagger_auto_schema(deprecated=True)
    def create(self, request):
        """todo: 获取URL但是不下载

        :param request:
        :return:
        """
        return

    @swagger_auto_schema(deprecated=True)
    def list(self, request):
        """
        """
        return

    @action(detail=False, methods=['post'])
    def download(self, request):
        """获取要下载图片的suit列表，并下载到文件夹"""
        suite_url = request.GET.get('suite_url', None)
        if not suite_url:
            return Response('no suite_url', status=status.HTTP_400_BAD_REQUEST)

        # 线程
        # todo: 同步可以执行，异步会timeout
        download_one_suit.delay(suite_url)
        return Response('delayed, check later', status=status.HTTP_202_ACCEPTED)


def index(request):

    return render(request, 'mzitu/index.html')
