#!/usr/bin/env python
# coding=utf-8

from celery import shared_task

from mzitu.runtimes.mzitu_suite import MzituSuite
from mzitu.runtimes.meituri_suite import MeituriSuite


@shared_task
def download_one_suite_mzitu(suite_url):
    mzitu_suite = MzituSuite(suite_url)
    mzitu_suite.get_one_suite_and_download()
    return


@shared_task
def download_one_suite_meituri(suite_url):
    meituri_suite = MeituriSuite(suite_url)
    meituri_suite.init()
    meituri_suite.get_imgs_and_download()
    return
