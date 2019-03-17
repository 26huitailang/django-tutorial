#!/usr/bin/env python
# coding=utf-8


import os
import shutil
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from mzitu.models.downloaded_suite import DownloadedSuite

logger = get_task_logger(__name__)


def mark_suite_without_local_files(suite_names: list = None):
    """标记有数据库记录但是没有本地文件的suite"""
    if suite_names is None:
        suite_names = []
    suite_objs = DownloadedSuite.objects.filter(name__in=suite_names).all()
    for obj in suite_objs:
        obj.is_complete = False
        obj.save()
    return


@shared_task
def delete_imgs():
    """定期删除数据库中没有记录的本地文件"""
    suite_name_list = DownloadedSuite.objects.values_list('name').all()
    suite_name_list = set([x[0] for x in suite_name_list])

    local_folders = os.listdir(settings.IMAGE_FOLDER_MZITU)
    local_folders = set([x for x in local_folders if os.path.isdir(os.path.join(settings.IMAGE_FOLDER_MZITU, x))])

    folder_to_delete = local_folders - suite_name_list
    for folder in folder_to_delete:
        folder_path = os.path.join(settings.IMAGE_FOLDER_MZITU, folder)
        shutil.rmtree(folder_path)
        logger.info("removed folder: %s", folder_path)

    suites_without_local_files = suite_name_list - local_folders
    mark_suite_without_local_files(list(suites_without_local_files))
    logger.info("mark these suites not complete: {}".format(suites_without_local_files))

    return
