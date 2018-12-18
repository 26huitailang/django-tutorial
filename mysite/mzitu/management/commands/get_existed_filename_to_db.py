import os
from django.core.management.base import BaseCommand
from mzitu.models.downloaded_suit import DownloadedSuit
from django.conf import settings

class Command(BaseCommand):
    help = '将已下载的套图信息放入数据库，下次好判断下载'

    def handle(self, *args, **options):
        for f in os.listdir(settings.IMAGE_FOLDER):
            f_path = os.path.join(settings.IMAGE_FOLDER, f)
            if os.path.isdir(f_path) and f != '__pycache__':
                suit = DownloadedSuit(
                    name=f,
                    url='',
                    max_page=len(os.listdir(f_path))
                )
                suit.save()
