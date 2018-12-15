# coding: utf-8

import random
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from mzitu.runtimes.proxy_ip import GetProxyIp
from mzitu.constants import (
    PROXY_SOURCE_URL,
    USER_AGENT_LIST,
)
from mzitu.runtimes.url_parser import MzituOneSuite, MzituThemePage
from mzitu.models import DownloadedSuit
from mzitu.serializers import MzituDownloadedSuitSerializer


class MzituSuitViewSet(GenericViewSet):
    serializer_class = MzituDownloadedSuitSerializer
    queryset = DownloadedSuit.objects.all()

    def create(self, request):
        """获取URL但是不下载

        :param request:
        :return:
        """
        return

    def list(self, request):
        """
        """
        return

    @action(detail=False, methods=['post'])
    def download(self, request):
        """获取要下载图片的suit列表，并下载到文件夹"""
        return


def index(request):

    return render(request, 'mzitu/index.html')


def parse_and_download_one_suit(request):

    suite_url = request.GET['suite_url']

    # 线程
    mzitu_one_suite = MzituOneSuite(suite_url)
    mzitu_one_suite.download_one_suit()

    return HttpResponse("下载完成")


def download_one_theme(request):
    theme_url = request.GET['theme_url']

    mzitu_theme = MzituThemePage(theme_url)
    suite_url_list = mzitu_theme.get_suite_urls_to_redis()
    for i in suite_url_list:
        mzitu_one_suite = MzituOneSuite(i)
        mzitu_one_suite.download_one_suit()

    return HttpResponse("下载完成")


def get_proxies(request):
    get_proxy_ip = GetProxyIp(PROXY_SOURCE_URL, random.choice(USER_AGENT_LIST))
    ip_list = get_proxy_ip.get_ip_list()
    get_proxy_ip.store_to_sqlite(ip_list)

    return HttpResponse('Downloaded')
