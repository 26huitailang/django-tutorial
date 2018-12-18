#!/usr/bin/env python
# coding=utf-8
import random
import time
import logging
import requests

from mzitu.constants import USER_AGENT_LIST
from mzitu.models.proxy_ip import ProxyIp
from mzitu.runtimes.proxy_ip import get_random_ip

logger = logging.getLogger(__name__)

# def generate_proxies(ip, port) -> str:
#     """构建proxy_url"""
#     proxy_url = "http://{}:{}".format(ip, port)
#     return proxy_url


def generate_proxies(ip, port) -> dict:
    """构建proxies"""
    proxies = {
        'http': 'http://{}:{}'.format(ip, port),
        'https': 'https://{}:{}'.format(ip, port),
    }
    return proxies


def requests_get(url, headers=None)-> requests.Response:
    """利用代理ip构建的requests.get请求"""
    ip, port = get_random_ip()
    proxies = generate_proxies(ip, port)
    try:
        result = requests.get(url, headers=headers, proxies=proxies, timeout=5)
    except TimeoutError:
        print("Timeout: {}".format(url))
        result = None

    return result


def proxy_request(url):
    """请求链接，返回页面html内容"""
    flag = True
    page = None

    while flag:
        ip, port = get_random_ip()
        try:
            time.sleep(0.5)
            proxies = generate_proxies(ip, port)
            response = requests.get(url, proxies=proxies, timeout=5)
        except (requests.exceptions.ProxyError, requests.exceptions.ReadTimeout) as e:
            logger.error(e)
            ProxyIp.set_score_change(ip, port, -1)
        else:
            flag = False
            page = response.content.decode('utf-8')
            response.connection.close()

    return page


def get_header(referer):
    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(USER_AGENT_LIST),
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headers
