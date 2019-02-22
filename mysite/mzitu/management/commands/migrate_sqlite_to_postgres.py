# coding: utf-8

from django.core.management.base import BaseCommand
from mzitu.models.downloaded_suite import DownloadedSuite, SuiteImageMap
from mzitu.models.tag import Tag
from django.conf import settings
import sqlite3
import os


class Command(BaseCommand):
    help = '从sqlite迁移表格到postgres'
    BASE_DIR = settings.BASE_DIR

    def handle(self, *args, **options):

        sql_file = os.path.join(self.BASE_DIR, 'local.sqlite3')
        print(sql_file)
        connection = sqlite3.connect(sql_file)
        c = connection.cursor()

        # downloadedsuite
        c.execute('select * from mzitu_downloadedsuite;')
        items = c.fetchall()
        for item in items:
            new_obj = DownloadedSuite(
                id=item[0],
                name=item[1],
                url=item[2],
                max_page=item[3],
                created_time=item[4],
                is_complete=item[5]
            )
            try:
                new_obj.save()
            except Exception as e:
                print(e)
                continue
        # tag
        c.execute('select * from mzitu_tag;')
        items = c.fetchall()
        for item in items:
            new_obj = Tag(
                id=item[0],
                is_like=item[1],
                url=item[2],
                name=item[3],
            )
            try:
                new_obj.save()
            except Exception as e:
                print(e)
                continue

        # downloadedsuite_tags
        # id, d_id, t_id
        for downloadedsuite in DownloadedSuite.objects.all():
            id_str = ''.join(str(downloadedsuite.id).split('-'))
            c.execute('select * from mzitu_downloadedsuite_tags where downloadedsuite_id="{}";'.format(id_str))
            items = c.fetchall()
            tag_id_list = [x[2] for x in items]
            tag_objs = Tag.objects.filter(id__in=tag_id_list).all()
            downloadedsuite.tags.set(tag_objs)

        # suiteimagemap
        c.execute('select * from mzitu_suiteimagemap;')
        items = c.fetchall()
        for item in items:
            # d_obj = DownloadedSuite.objects.get(id=item[3])
            new_obj = SuiteImageMap(
                id=item[0],
                url=item[1],
                image=item[2],
                suite_id=item[3],
            )
            try:
                new_obj.save()
            except Exception as e:
                print(e)
                continue
