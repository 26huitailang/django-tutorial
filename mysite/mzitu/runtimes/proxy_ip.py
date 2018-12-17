#!/usr/bin/python
# coding: utf-8

from mzitu.models.proxy_ip import ProxyIp


def get_random_ip():
    """获得随机的代理ip"""
    item = ProxyIp.get_proxy_ip_valid()
    proxy_ip = (item.ip, item.port)
    # (1, '211.147.67.150', '80', 1)  id, ip, port, is_valid
    return proxy_ip
