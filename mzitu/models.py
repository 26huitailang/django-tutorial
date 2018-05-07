import uuid

from django.db import models
from django.utils import timezone


class ProxyIp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.CharField(max_length=16)
    port = models.IntegerField()
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(default=timezone.now)
