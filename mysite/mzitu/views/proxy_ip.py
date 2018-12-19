# coding: utf-8

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from mzitu.models.proxy_ip import ProxyIp
from mzitu.serializers import MzituDownloadedSuitSerializer
from mzitu.tasks.proxy_ip import get_proxy_ips_and_insert_db


class ProxyIpViewSet(GenericViewSet):
    serializer_class = MzituDownloadedSuitSerializer
    queryset = ProxyIp.objects.all()

    def create(self, request):
        """获取新的proxy ip"""
        # todo: 异步任务，之前是class，分解为function，celery目前推荐的用法
        get_proxy_ips_and_insert_db.delay()

        return Response('accepted, check later', status=status.HTTP_202_ACCEPTED)

    # @action(detail=False, methods=['post'])
    # def check_valid(self, request):
    #     """标记失效的代理"""
    #     return
