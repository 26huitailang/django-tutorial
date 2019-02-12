# coding: utf-8

from django.core.management.base import BaseCommand
from mzitu.models.downloaded_suite import DownloadedSuite
from django.conf import settings
import shutil
import os


class Command(BaseCommand):
    help = '将测试websocket用的图置为初始状态，未完成并删除本地文件'

    def handle(self, *args, **options):
        suite_id = '965e4a33a14b4645abafadfe0e6cb93a'
        suite = DownloadedSuite.objects.get(id=suite_id)
        suite.is_complete = False
        suite.save()

        folder = os.path.join(settings.IMAGE_FOLDER, suite.name)
        shutil.rmtree(folder)
        os.mkdir(folder)
        print(f'已删除重建 {folder}')
