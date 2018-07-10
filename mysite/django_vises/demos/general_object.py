#!/usr/bin/env python
# coding=utf-8


from django_vises.models.general_object import GeneralObject


def demo():
    obj = GeneralObject.objects.get_queryset_by_group_and_key(group=1, key=2).filter(
        value={'owner': 'Bob'}
    ).first()

    return obj
