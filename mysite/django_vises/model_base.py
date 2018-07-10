#!/usr/bin/env python
# coding=utf-8


from uuid import uuid4
import logging

from django.db import models


__all__ = ['ModelBaseObject', 'ModelBaseRecord']

logger = logging.getLogger(__name__)


class ModelBaseObjectNoId(models.Model):
    """基本数据库模式 - 对象型 - 无 id
    创建时间，最后更新时间，需要继承者自行实现 __str__()
    """
    time_created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    time_last_updated = models.DateTimeField(
        auto_now=True,
        db_index=True,
    )

    class Meta(object):
        abstract = True


class ModelBaseObject(ModelBaseObjectNoId):
    """基本数据库模型 - 对象型
    id, 创建时间，最后更新时间
    """
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid4,
    )

    class Meta(object):
        abstract = True

    def __str__(self):
        return '{}'.format(self.id)


class ModelBaseRecord(models.Model):
    """基本数据库模式 - 记录/日志型
    创建时间，无更新需求
    """
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid4,
    )

    time_created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta(object):
        abstract = True

    def __str__(self):
        return '{}'.format(self.id)
