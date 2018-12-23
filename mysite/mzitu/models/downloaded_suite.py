import uuid

from django.db import models
from django.utils import timezone


class DownloadedSuite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60)
    url = models.URLField(max_length=200)
    max_page = models.IntegerField()
    tag = models.CharField(max_length=100, default='')  # 存一个list试试
    created_time = models.DateTimeField(default=timezone.now)
    # todo: 增加一个folder path，media_root + this-folder = full-path


class SuiteImageMap(models.Model):
    # todo: 还没有应用
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    suite = models.ForeignKey(DownloadedSuite, related_name='images', on_delete=models.CASCADE)
    url = models.URLField(max_length=300)
    image = models.ImageField(blank=True, unique=True)

    @classmethod
    def get_image_path(cls, suite_name, filename):
        # todo: 可以用pre_save等做预处理
        print(suite_name, filename)
        return '/'.join(['mzitu', suite_name, filename])