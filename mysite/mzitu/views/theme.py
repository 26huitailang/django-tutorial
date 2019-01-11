# coding: utf-8

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from mzitu.models.downloaded_suite import DownloadedSuite
from mzitu.serializers import MzituDownloadedSuiteSerializer
from mzitu.tasks.theme import download_one_theme


class MzituThemeViewSet(GenericViewSet):
    serializer_class = MzituDownloadedSuiteSerializer
    queryset = DownloadedSuite.objects

    def create(self, request):
        """获取主题但不下载"""
        return

    def list(self, request):
        """套图列表"""
        return

    @action(detail=False, methods=['post'])
    def download(self, request):
        """获取要下载图片的suit列表，并下载到文件夹"""
        # debug, socket timeout 全部delay为一个task
        theme_url = request.GET['theme_url']
        download_one_theme.delay(theme_url)

        return Response('delayed, please check later: {}'.format(theme_url),
                        status=status.HTTP_202_ACCEPTED)
