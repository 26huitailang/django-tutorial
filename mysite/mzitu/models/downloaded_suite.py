import os
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

from mzitu.models.tag import Tag


class DownloadedSuite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, unique=True)
    url = models.URLField(max_length=200, unique=True)
    max_page = models.IntegerField()
    tags = models.ManyToManyField(Tag)
    created_time = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(verbose_name='完整性', default=False)
    Choices = {
        'mzitu': 'mzitu',
        'meituri': 'meituri',
    }

    class Meta:
        ordering = ['-created_time']

    @classmethod
    def is_url_exist(cls, url) -> (bool, object):
        item = cls.objects.filter(url=url).first()
        if item:
            return True, item
        return False, None

    @classmethod
    def is_url_completed(cls, url) -> bool:
        item = cls.objects.filter(url=url).first()
        if item:
            return item.is_complete
        return False

    def get_suite_folder_path(self) -> str or None:
        """返回不同的对象的folder路径"""
        if self.Choices['meituri'] in self.url:
            if not self.images:
                return None
            org = self.images.first().image.name.split('/')[1]
            return os.path.join(settings.IMAGE_FOLDER_MEITURI, org, self.name)
        elif self.Choices['mzitu'] in self.url:
            return os.path.join(settings.IMAGE_FOLDER_MZITU, self.name)

        return None

    def __str__(self):
        return "{} {} {} {}".format(
            self.created_time,
            self.name,
            [x.name for x in self.tags.all()],
            self.url,
        )


class SuiteImageMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    suite = models.ForeignKey(DownloadedSuite, related_name='images', on_delete=models.CASCADE)
    url = models.URLField(max_length=300)
    image = models.ImageField(blank=True, unique=True)

    class Meta:
        ordering = ['image']

    @classmethod
    def get_image_path(cls, root_name, suite_name, filename, **kwargs):
        """获得存储的image字段，mzitu/Gakki/01.jpg

        :param root_name: mzitu/meituri
        :param suite_name: suite 标题
        :param filename: 文件名字不含路径
        """
        # todo: 可以用pre_save等做预处理
        # meituri，多一个org路径
        print(suite_name, filename)
        if 'org' in kwargs:
            print(kwargs['org'])
            return '/'.join([root_name, kwargs['org'], suite_name, filename])
        return '/'.join([root_name, suite_name, filename])

    def __str__(self):
        return "{} {}".format(self.suite.name, self.image)
