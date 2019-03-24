#!/usr/bin/env python
# coding=utf-8

from celery import shared_task

from mzitu.runtimes.mztiu_theme import get_suite_urls_to_redis
from mzitu.runtimes.mzitu_suite import MzituSuite
from mzitu.runtimes.meituri_suite import MeituriTheme, MeituriSuite


@shared_task
def download_one_theme(theme_url):
    suite_url_list = get_suite_urls_to_redis(theme_url)
    for suite in suite_url_list:
        # todo: 暂时顺序执行
        mzitu_suite = MzituSuite(suite)
        mzitu_suite.get_one_suite_and_download()
    return


@shared_task
def download_one_theme_meituri(theme_url):
    meituri_theme = MeituriTheme(theme_url)
    meituri_theme.init()
    meituri_theme.get_all_suite_urls_to_queue()

    while not meituri_theme.suite_queue.empty():
        _s_url = meituri_theme.suite_queue.get()
        meituri_suite = MeituriSuite(_s_url)
        meituri_suite.init()
        meituri_suite.get_imgs_and_download()
    return
