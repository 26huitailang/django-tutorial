# coding: utf-8

from django.core.management.base import BaseCommand
from mzitu.runtimes.meituri_suite import MeituriSuite


class Command(BaseCommand):
    help = '将测试websocket用的图置为初始状态，未完成并删除本地文件'

    def handle(self, *args, **options):
        suite_url = 'https://www.meituri.com/a/25133/'

        meituri_suite = MeituriSuite(suite_url)
        meituri_suite.init_with_first_page()
        meituri_suite.get_imgs_and_download()
        return
