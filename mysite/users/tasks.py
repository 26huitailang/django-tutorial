#!/usr/bin/env python
# coding=utf-8

"""
celery example
"""

from celery import shared_task
from celery.utils.log import get_task_logger

from mysite.celery import app
from django.contrib.auth.models import User

logger = get_task_logger(__file__)


class AddTwoTask(app.Task):

    def run(self, x, y):
        resp = self._add_two_nums(x, y)
        logger.info(resp)
        # can use orm
        logger.info([x.username for x in User.objects.all()])

    def _add_two_nums(self, x, y):
        return x + y


add_two_nums = app.register_task(AddTwoTask())


@shared_task
def add_two(x, y):
    return x + y
