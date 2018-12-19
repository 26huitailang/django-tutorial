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
from mzitu.runtimes.suite import generate_proxies

logger = get_task_logger(__name__)


def _get_proxy_ip_list():
    """从网站获取proxy_ip list，并存入DB"""
    # todo: 获取更多的代理ip，现在仅获取了首页
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

    return ip_list


@shared_task
def get_proxy_ips_and_insert_db():
    """for api"""
    ip_list = _get_proxy_ip_list()
    for ip_tuple in ip_list:
        ProxyIp.insert_proxy_ip(ip_tuple[0], ip_tuple[1])
    return


# todo: shared_task 不能通过app.on_after_configure.connect 注册
@shared_task
def get_proxy_ips_crontab():
    """for crontab"""
    # 获取并插入数据库
    ip_list = _get_proxy_ip_list()
    logger.info("insert ProxyIp: %s", len(ip_list))
    for ip_tuple in ip_list:
        ProxyIp.insert_proxy_ip(ip_tuple[0], ip_tuple[1])

    # 定时删除，后删除可以避免周期内重复的但是无效的代理又进入数据库
    count = ProxyIp.delete_invalid_items()
    logger.info("delete ProxyIp: %s", count)
    return


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
            r = requests.get(url, proxies=generate_proxies(item.ip, item.port), timeout=(4, 30))
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
