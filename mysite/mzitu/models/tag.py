import uuid

from django.db import models


class Tag(models.Model):
    """Tag of suite"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    is_like = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.name, self.is_like)
