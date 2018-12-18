#!/usr/bin/python
# coding: utf-8

from mzitu.models.proxy_ip import ProxyIp


def get_random_ip():
    """获得随机的代理ip"""
    item = ProxyIp.get_valid_random_proxy_ip()
    proxy_ip = (item.ip, item.port)
    return proxy_ip
