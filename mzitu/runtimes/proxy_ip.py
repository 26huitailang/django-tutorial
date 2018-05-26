#!/usr/bin/python
# coding: utf-8

# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用

import requests
from bs4 import BeautifulSoup

from .sqlite import (
    insert_proxy_ip,
    get_proxy_ip_valid,
    mark_proxy_ip_not_valid,
)


class GetProxyIp:
    def __init__(self, url, user_agent):
        self.url = url
        self.headers = {
            'User-Agent': user_agent
        }

    def get_ip_list(self):
        web_data = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        ips = soup.find_all('tr')
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append((tds[1].text, tds[2].text))
        # print(ip_list)
        return ip_list

    @staticmethod
    def store_to_sqlite(ip_list):
        """
        获取的信息存入sqlite

        :param ip_list: [(ip, port)]
        :return:
        """
        for ip_tuple in ip_list:
            print(ip_tuple)
            insert_proxy_ip(ip_tuple[0], ip_tuple[1])

    @staticmethod
    def get_random_ip():
        item = get_proxy_ip_valid()
        proxy_ip = (item.ip, item.port)
        print(proxy_ip)
        # (1, '211.147.67.150', '80', 1)  id, ip, port, is_valid
        return proxy_ip

    @staticmethod
    def mark_invalid_proxy_ip(ip, port):
        mark_proxy_ip_not_valid(ip, port)
