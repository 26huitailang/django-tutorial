import uuid
import random
from django.db import models
from django.utils import timezone


class ProxyIp(models.Model):
    """代理ip"""
    INITIAL_SCORE = 10
    MIN_SCORE = 0
    MAX_SCORE = 100

    # fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(default=timezone.now)
    ip = models.CharField(max_length=16)
    port = models.IntegerField()
    # 分数，满分100，新获取的为10分，检测通过设置为100分，失败-1，成功+1，到0的话标记为无效，定期移除
    score = models.PositiveSmallIntegerField(verbose_name='分数', default=INITIAL_SCORE)
    is_valid = models.BooleanField(default=True)

    @classmethod
    def get_valid_random_proxy_ip(cls):
        """获得一个有效的proxy_ip"""
        items = ProxyIp.objects.filter(is_valid=True).order_by('-score').all()[:5]
        try:
            item = random.choice(items)
        except IndexError:
            raise(IndexError('没有有效的代理ip，请重新补充'))

        return item

    @classmethod
    def set_proxy_ip_not_valid(cls, ip, port):
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
        if item:
            return item
        item = ProxyIp.objects.create(ip=ip, port=port)
        return item

    @classmethod
    def set_score_change(cls, ip, port, change_value: int = 0):
        item = ProxyIp.objects.filter(ip=ip, port=port).first()
        if item:
            item.score += change_value
            item.save()
        return item

    @classmethod
    def set_score_max(cls, ip, port):
        item = ProxyIp.objects.filter(ip=ip, port=port).first()
        if item:
            item.score = cls.MAX_SCORE
            item.save()
        return item

    @classmethod
    def delete_invalid_items(cls):
        count, _ = ProxyIp.objects.filter(is_valid=False).delete()
        return count
