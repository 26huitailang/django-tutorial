# coding: utf-8

from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from mzitu.models.downloaded_suite import DownloadedSuite
from mzitu.serializers import MzituDownloadedSuiteSerializer
from mzitu.tasks.suite import download_one_suite


class MzituSuiteViewSet(GenericViewSet):
    serializer_class = MzituDownloadedSuiteSerializer
    queryset = DownloadedSuite.objects.all()

    @swagger_auto_schema(deprecated=True)
    def create(self, request):
        """todo: 获取URL但是不下载，如果要实现这个功能的话，需要修改suite的task流程，现在是下载后才持久化img_url

        :param request:
        :return:
        """
        return

    def retrieve(self, request, pk: str = None):
        """Suite detail
        """
        item = self.queryset.get(id=pk)
        serializer = MzituDownloadedSuiteSerializer(item)
        return Response(serializer.data)

    def list(self, request):
        """Suite list
        """
        serializer = MzituDownloadedSuiteSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def download(self, request):
        """获取要下载图片的suite列表，并下载到文件夹"""
        # todo: 改为form或者post body
        suite_url = request.GET.get('suite_url', None)
        if not suite_url:
            return Response('no suite_url', status=status.HTTP_400_BAD_REQUEST)

        # 线程
        # fix: 同步可以执行，异步会timeout
        download_one_suite.delay(suite_url)
        # download_one_suite(suite_url)
        return Response('delayed, check later', status=status.HTTP_202_ACCEPTED)


def index(request):

    return render(request, 'mzitu/index.html')
