# coding: utf-8

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from mzitu.models.downloaded_suit import DownloadedSuit
from mzitu.serializers import MzituDownloadedSuitSerializer
from mzitu.runtimes.theme import get_suite_urls_to_redis
from mzitu.tasks.suite import download_one_suite

class MzituThemeViewSet(GenericViewSet):
    serializer_class = MzituDownloadedSuitSerializer
    queryset = DownloadedSuit.objects.all()

    def create(self, request):
        """获取主题但不下载"""
        return

    def list(self, request):
        """套图列表"""
        return

    @action(detail=False, methods=['post'])
    def download(self, request):
        """获取要下载图片的suit列表，并下载到文件夹"""
        # todo: debug, socket timeout 问题
        theme_url = request.GET['theme_url']
        suite_url_list = get_suite_urls_to_redis(theme_url)
        for suite in suite_url_list:
            download_one_suite.delay(suite)
        return Response({'message': 'delayed {}'.format(len(suite_url_list)), 'themes': suite_url_list},
                        status=status.HTTP_202_ACCEPTED)
