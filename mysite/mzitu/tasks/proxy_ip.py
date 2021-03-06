#!/usr/bin/python
# coding: utf-8

"""
IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
仅仅爬取首页IP地址就足够一般使用
"""

import random
import requests
from requests_html import HTMLSession, HTMLResponse
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.db import connections
from concurrent.futures import ThreadPoolExecutor

from mysite.sentry import client as sentry_client
from mzitu.constants import USER_AGENT_LIST
from mzitu.models.proxy_ip import ProxyIp
from mzitu.runtimes.mzitu_suite import generate_proxies


logger = get_task_logger(__name__)


def _get_proxy_ip_list():
    """从网站获取proxy_ip list，并存入DB"""
    # todo: 获取更多的代理ip，现在仅获取了首页
    headers = {'User-Agent': random.choice(USER_AGENT_LIST)}
    session = HTMLSession()
    session_resp = session.get(settings.PROXY_SOURCE_URL, headers=headers, timeout=5)
    assert isinstance(session_resp, HTMLResponse)
    ips = session_resp.html.find('tr')
    ip_list = []
    for ip_info in ips[1:]:
        tds = ip_info.find('td')
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


def _update_proxy_ip_score(proxy_ip_instance, url):
    """更新每个proxy ip的分数，为0标记为is_valid=False"""
    valid = True
    try:
        r = requests.get(url, proxies=generate_proxies(proxy_ip_instance.ip, proxy_ip_instance.port), timeout=(4, 12))
    except Exception as e:
        logger.warning(e)
        sentry_client.capture_exceptions()
        valid = False
    else:
        try:
            # API返回结果有变化
            result = r.json()['origin'].split(',')[0].strip()
            valid = True if proxy_ip_instance.ip == result else False
        except Exception as e:
            logger.warning(e)
            valid = False
    finally:
        if valid:
            if proxy_ip_instance.score < 100 and proxy_ip_instance.score != 10:
                logger.info("加1: %s", proxy_ip_instance.ip)
                proxy_ip_instance.score += 1
            elif proxy_ip_instance.score == 10:
                logger.info("设为100: %s", proxy_ip_instance.ip)
                proxy_ip_instance.score = 100
        else:  # invalid
            if proxy_ip_instance.score > 0:
                logger.info("减1: %s", proxy_ip_instance.ip)
                proxy_ip_instance.score -= 1
            else:
                logger.info("失效: %s", proxy_ip_instance.ip)
                proxy_ip_instance.is_valid = False
        proxy_ip_instance.save()
    return


def on_done(future):
    """Django 关闭连接的时机是和请求的连接一起关闭
    这里是通过线程使用，就不会关闭导致连接堆积，PG不接受新连接

    解决：注册这个回调，在每个线程执行完后执行关闭连接的操作。
    """
    connections.close_all()
    return


@shared_task
def check_proxy_ip():
    """测试代理ip是否有效

    如果是10分可用的话，标记为100分，其他按是否有效+/-1分
    如果为0分，则标记为not valid
    """
    # todo!!!: 总是检查失败，是不是代码有问题？
    # MAX_WORKERS = 10
    url = 'http://httpbin.org/ip'
    items = ProxyIp.objects.filter(is_valid=True).order_by('created_time').all()
    # todo: 多线程，但是控制数量
    with ThreadPoolExecutor() as executor:
        for item in items:
            future = executor.submit(_update_proxy_ip_score, item, url)
            future.add_done_callback(on_done)

    # 27s -> 17s
    # task_list = [gevent.spawn(_update_proxy_ip_score, item, url) for item in items]
    # gevent.joinall(task_list)
    return
