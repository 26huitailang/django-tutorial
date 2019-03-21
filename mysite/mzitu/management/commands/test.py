# coding: utf-8

from django.core.management.base import BaseCommand
from mzitu.runtimes.meituri_suite import MeituriSuite, MeituriTheme


class Command(BaseCommand):
    help = '将测试websocket用的图置为初始状态，未完成并删除本地文件'

    def handle(self, *args, **options):
        suite_url = 'https://www.meituri.com/a/25133/'
        theme_url = 'https://www.meituri.com/x/49/index_24.html'

        # suite
        # meituri_suite = MeituriSuite(suite_url)
        # meituri_suite.init()
        # meituri_suite.get_imgs_and_download()

        # theme
        meituri_theme = MeituriTheme(theme_url)
        meituri_theme.init()
        meituri_theme.get_all_suite_urls_to_queue()

        while not meituri_theme.suite_queue.empty():
            _s_url = meituri_theme.suite_queue.get()
            meituri_suite = MeituriSuite(_s_url)
            meituri_suite.init()
            meituri_suite.get_imgs_and_download(do_download=False)

        return
