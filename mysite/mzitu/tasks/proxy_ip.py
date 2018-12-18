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
from mzitu.runtimes.suit import generate_proxies

logger = get_task_logger(__name__)


@shared_task
def get_ip_list():
    """从网站获取proxy_ip list，并存入DB"""
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


@shared_task
def check_proxy_ip():
    """测试代理ip是否有效

    如果是10分可用的话，标记为100分，其他按是否有效+/-1分
    如果为0分，则标记为not valid
    """
    # todo: 检查代理ip有效性的定时任务
    url = 'http://httpbin.org/ip'
    items = ProxyIp.objects.filter(is_valid=True).order_by('created_time').all()
    for item in items:
        valid = True
        try:
            r = requests.get(url, proxies=generate_proxies(item.ip, item.port), timeout=4)
        except Exception as e:
            logger.warning(e)
            valid = False
        else:
            try:
                result = r.json()['origin']
                valid = True if item.ip == result else False
            except Exception as e:
                logger.warning(e)
                valid = False
        finally:
            if valid:
                if item.score < 100 and item.score != 10:
                    logger.info("加1: %s", item.ip)
                    item.score += 1
                elif item.score == 10:
                    logger.info("设为100: %s", item.ip)
                    item.score = 100
            else:  # invalid
                if item.score > 0:
                    logger.info("减1: %s", item.ip)
                    item.score -= 1
                else:
                    logger.info("失效: %s", item.ip)
                    item.is_valid = False
            item.save()
