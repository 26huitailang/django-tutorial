import os
from django.core.management.base import BaseCommand
from mzitu.models import DownloadedSuit
from mzitu.constants import IMAGE_FOLDER


class Command(BaseCommand):
    help = '将已下载的套图信息放入数据库，下次好判断下载'

    def handle(self, *args, **options):
        for f in os.listdir(IMAGE_FOLDER):
            f_path = os.path.join(IMAGE_FOLDER, f)
            if os.path.isdir(f_path) and f != '__pycache__':
                suit = DownloadedSuit(
                    name=f,
                    url='',
                    max_page=len(os.listdir(f_path))
                )
                suit.save()
