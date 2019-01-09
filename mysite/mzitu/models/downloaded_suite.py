import uuid

from django.db import models
from django.utils import timezone
from mzitu.models.tag import Tag


class DownloadedSuite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, unique=True)
    url = models.URLField(max_length=200,unique=True)
    max_page = models.IntegerField()
    tags = models.ManyToManyField(Tag)
    created_time = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(name='完整性', default=True)

    class Meta:
        ordering = ['-created_time']

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
    def get_image_path(cls, suite_name, filename):
        # todo: 可以用pre_save等做预处理
        print(suite_name, filename)
        return '/'.join(['mzitu', suite_name, filename])

    def __str__(self):
        return "{} {}".format(self.suite.name, self.image)
