#!/usr/bin/env python
# coding=utf-8

from celery import shared_task

from mzitu.runtimes.mztiu_theme import get_suite_urls_to_redis
from mzitu.tasks.suite import MzituSuite


@shared_task
def download_one_theme(theme_url):
    suite_url_list = get_suite_urls_to_redis(theme_url)
    for suite in suite_url_list:
        # todo: 暂时顺序执行
        mzitu_suite = MzituSuite(suite)
        mzitu_suite.get_one_suite_and_download()
    return
