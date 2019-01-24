# coding: utf-8

import json
from django.shortcuts import get_object_or_404
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
    # FBI Warning: 这里用.all()获取的话，会导致修改数据更新不及时
    queryset = DownloadedSuite.objects

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
        serializer = MzituDownloadedSuiteSerializer(self.queryset.all(), many=True)
        # 这里存在读取和sqlite数据不一致的问题，调用删除后，不重启应用，会读到已删除的suite对象，不过关联的字段都是空的
        # 不要在queryset提前获取数据
        resp = serializer.data
        return Response(resp)

    def destroy(self, request, pk: str = None):
        """delete one, local files will delete crontab with celery"""
        item = get_object_or_404(DownloadedSuite, id=pk)
        delete_info = item.delete()
        return Response(json.dumps(delete_info), status=status.HTTP_202_ACCEPTED)

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
