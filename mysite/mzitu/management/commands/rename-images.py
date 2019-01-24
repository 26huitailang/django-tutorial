# coding: utf-8

from django.core.management.base import BaseCommand
from mzitu.models.downloaded_suite import SuiteImageMap, DownloadedSuite


class Command(BaseCommand):
    help = '重命名图片'

    def handle(self, *args, **options):
        suite_id = '79a727a3e3ce41ce8ff3ff5200f9d694'
        suit_instance = DownloadedSuite.objects.get(id=suite_id)
        for i in range(1, 47):
            fake_image_base = 'mzitu/Gakki/{:0>2d}.jpg'
            fake_url = 'https://i.meizitu.net/2018/12/09a25.jpg'
            item = SuiteImageMap(
                url=fake_url,
                image=fake_image_base.format(i),
                suite=suit_instance,
            )
            item.save()
            print(item.image.path)
