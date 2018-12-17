# coding: utf-8

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from mzitu.models.downloaded_suit import DownloadedSuit
from mzitu.serializers import MzituDownloadedSuitSerializer


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
        return
