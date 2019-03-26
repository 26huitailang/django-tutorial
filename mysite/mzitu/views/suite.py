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
from mzitu.tasks.suite import (
    download_one_suite_mzitu,
    download_one_suite_meituri,
)
from mzitu.runtimes.mzitu_suite import MzituSuite
from mzitu.runtimes.meituri_suite import MeituriSuite


class MzituSuiteViewSet(GenericViewSet):
    serializer_class = MzituDownloadedSuiteSerializer
    # FBI Warning: 这里用.all()获取的话，会导致修改数据更新不及时
    queryset = DownloadedSuite.objects
    page_size_query_param = 'page_size'

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
        page = self.paginate_queryset(self.queryset.all())
        if page:
            serializer = MzituDownloadedSuiteSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
        suite_url = request.data.get('suite_url', None)
        if not suite_url:
            return Response('no suite_url', status=status.HTTP_400_BAD_REQUEST)

        if MeituriSuite.check_suite_url(suite_url):
            download_one_suite_meituri.delay(suite_url)
        elif MzituSuite.check_suite_url(suite_url):
            download_one_suite_mzitu.delay(suite_url)
            # download_one_suite_mzitu(suite_url)
        return Response('delayed, check later', status=status.HTTP_202_ACCEPTED)
