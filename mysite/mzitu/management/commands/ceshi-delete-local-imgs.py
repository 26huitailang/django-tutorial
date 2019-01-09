# coding: utf-8

from django.core.management.base import BaseCommand
from mzitu.tasks.local_imgs import delete_imgs


class Command(BaseCommand):
    help = '测试代理ip'

    def handle(self, *args, **options):
        delete_imgs()
