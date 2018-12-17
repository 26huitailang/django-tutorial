#!/usr/bin/python
# coding: utf-8

"""
IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
仅仅爬取首页IP地址就足够一般使用
"""

import random
import requests
from bs4 import BeautifulSoup
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from mzitu.constants import USER_AGENT_LIST
from mzitu.models.proxy_ip import ProxyIp

logger = get_task_logger(__name__)


@shared_task
def update_ip_list():
    """更新proxy_ip list"""
    headers = {'User-Agent': random.choice(USER_AGENT_LIST)}
    web_data = requests.get(settings.PROXY_SOURCE_URL, headers=headers, timeout=5)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append((tds[1].text, tds[2].text))
    logger.info(ip_list)

    for ip_tuple in ip_list:
        ProxyIp.insert_proxy_ip(ip_tuple[0], ip_tuple[1])
