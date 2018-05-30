import random
from django.shortcuts import render
from django.http import HttpResponse

from mzitu.runtimes.proxy_ip import GetProxyIp
from mzitu.constants import (
    PROXY_SOURCE_URL,
    USER_AGENT_LIST,
)
from mzitu.runtimes.url_parser import download_one_suit
from mzitu.runtimes.asyncio_for_mzitu import async_get_images_urls


def index(request):

    return render(request, 'mzitu/index.html')


def parse_and_download_one_suit(request):

    suit_url = request.GET['suit_url']

    # 线程
    download_one_suit(suit_url)

    return HttpResponse("下载完成")


def get_proxies(request):
    get_proxy_ip = GetProxyIp(PROXY_SOURCE_URL, random.choice(USER_AGENT_LIST))
    ip_list = get_proxy_ip.get_ip_list()
    get_proxy_ip.store_to_sqlite(ip_list)

    return HttpResponse('Downloaded')


def async_parse_and_download_one_suit(request):

    suit_url = request.GET['suit_url']

    # 线程
    async_get_images_urls(suit_url)

    return HttpResponse("下载完成")