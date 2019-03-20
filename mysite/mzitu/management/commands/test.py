# coding: utf-8

from django.core.management.base import BaseCommand
from mzitu.runtimes.meituri_suite import MeituriSuite, MeituriTheme


class Command(BaseCommand):
    help = '将测试websocket用的图置为初始状态，未完成并删除本地文件'

    def handle(self, *args, **options):
        suite_url = 'https://www.meituri.com/a/25133/'
        theme_url = 'https://www.meituri.com/x/49/'

        # suite
        # meituri_suite = MeituriSuite(suite_url)
        # meituri_suite.init()
        # meituri_suite.get_imgs_and_download()

        # theme
        meituri_theme = MeituriTheme(theme_url)
        meituri_theme.init()
        return
