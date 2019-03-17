# coding: utf-8

from django.core.management.base import BaseCommand
import requests
from mzitu.runtimes.mzitu_suite import generate_proxies


class Command(BaseCommand):
    help = '测试代理ip'

    def handle(self, *args, **options):
        url = 'http://httpbin.org/ip'
        ip = '219.234.5.128'
        port = '3128'
        r = requests.get(url, proxies=generate_proxies(ip, port))
        print(r.text)
        assert ip == r.json()['origin']
