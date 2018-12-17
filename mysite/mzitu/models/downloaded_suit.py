import uuid

from django.db import models
from django.utils import timezone


class DownloadedSuit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60)
    url = models.URLField(max_length=200)
    max_page = models.IntegerField()
    tag = models.CharField(max_length=100, default='')  # 存一个list试试
    # todo: 增加一个folder path，media_root + this-folder = full-path

class SuitImageMap(models.Model):
    # todo: 还没有应用
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    suit = models.ForeignKey(DownloadedSuit, on_delete=models.CASCADE)
    url = models.URLField(max_length=300)
