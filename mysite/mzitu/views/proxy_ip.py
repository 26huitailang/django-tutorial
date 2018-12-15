# coding: utf-8

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from mzitu.models import ProxyIp
from mzitu.serializers import MzituDownloadedSuitSerializer


class ProxyIpViewSet(GenericViewSet):
    serializer_class = MzituDownloadedSuitSerializer
    queryset = ProxyIp.objects.all()

    def create(self, request):
        """获取新的proxy ip"""
        return

    @action(detail=False, methods=['post'])
    def check_valid(self, request):
        """标记失效的代理"""
        return
