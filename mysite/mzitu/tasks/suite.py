#!/usr/bin/env python
# coding=utf-8

from celery import shared_task

from mzitu.runtimes.mzitu_suite import MzituSuite


@shared_task
def download_one_suite(suite_url):
    mzitu_suite = MzituSuite(suite_url)
    mzitu_suite.get_one_suite_and_download()
    return
