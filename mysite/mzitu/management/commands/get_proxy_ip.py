# coding: utf-8

from django.core.management.base import BaseCommand
from mzitu.tasks.proxy_ip import get_proxy_ips_and_insert_db


class Command(BaseCommand):
    help = '获得代理IP'

    def handle(self, *args, **options):
        for i in range(10):
            get_proxy_ips_and_insert_db.delay()
        print('finish')
