# coding: utf-8

from django.core.management.base import BaseCommand
from mzitu.runtimes.meituri_suite import MeituriSuite, MeituriTheme
from mzitu.tasks.proxy_ip import get_proxy_ips_and_insert_db


class Command(BaseCommand):
    help = '测试最近开发的功能'

    def handle(self, *args, **options):
        suite_url = 'https://www.meituri.com/a/25133/'
        theme_url = 'https://www.meituri.com/x/49/index_24.html'

        # get_proxy_ips_and_insert_db()

        # suite
        meituri_suite = MeituriSuite(suite_url)
        meituri_suite.init()
        # meituri_suite.get_imgs_and_download()
        meituri_suite.check_and_mark_suite_complete()

        # theme
        # meituri_theme = MeituriTheme(theme_url)
        # meituri_theme.init()
        # meituri_theme.get_all_suite_urls_to_queue()

        # while not meituri_theme.suite_queue.empty():
        #     _s_url = meituri_theme.suite_queue.get()
        #     meituri_suite = MeituriSuite(_s_url)
        #     meituri_suite.init()
        #     meituri_suite.get_imgs_and_download(do_download=False)

        return
