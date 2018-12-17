import uuid

from django.db import models
from django.utils import timezone


class ProxyIp(models.Model):
    """代理ip"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.CharField(max_length=16)
    port = models.IntegerField()
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(default=timezone.now)

    @classmethod
    def get_proxy_ip_valid(cls):
        """获得一个有效的proxy_ip"""
        item = ProxyIp.objects.filter(is_valid=True).first()

        return item

    @classmethod
    def mark_proxy_ip_not_valid(cls, ip, port):
        """标记一个失效的proxy_ip"""
        item = ProxyIp.objects.filter(ip=ip, port=port).first()
        if item:
            item.is_valid = 0
            item.save()
            return item
        return None

    @classmethod
    def insert_proxy_ip(cls, ip, port):
        """插入一个proxy_ip"""
        item = ProxyIp.objects.filter(ip=ip, port=port).first()
        if not item:
            item = ProxyIp.objects.create(ip=ip, port=port)
            return item
        return None
