# coding: utf-8

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from mzitu.models.tag import Tag
from mzitu.serializers import (
    TagSerializer,
    MzituDownloadedSuiteSerializer,
)


class TagViewSet(GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects

    def list(self, request):
        """tag list"""
        page = self.paginate_queryset(self.queryset.order_by('-is_like', 'name'))
        if page:
            # 如果 self 没有 paginator 的话 page 为 None
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset.order_by('-is_like', 'name'), many=True)
        return Response(serializer.data)

    def destroy(self, request, pk: str = None):
        """delete one tag by id"""
        instance = get_object_or_404(Tag, id=pk)
        suite_count_with_tag = instance.downloadedsuite_set.count()
        if suite_count_with_tag != 0:
            return Response('still have suites {}'.format(suite_count_with_tag),
                            status=status.HTTP_400_BAD_REQUEST)

        if instance.is_like:
            return Response('is like {}'.format(instance.is_like),
                            status=status.HTTP_400_BAD_REQUEST)

        instance.delete()
        return Response('deleted {}'.format(instance.name),
                        status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get'])
    def suites(self, request, pk: str = None):
        instance = get_object_or_404(Tag, id=pk)
        suite_instances = instance.downloadedsuite_set.order_by('-created_time').all()
        serializer = MzituDownloadedSuiteSerializer(suite_instances, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like_toggle(self, request, pk: str = None):
        """标记like"""
        instance = get_object_or_404(Tag, id=pk)
        instance.is_like = not instance.is_like
        instance.save()
        return Response(self.get_serializer(instance).data,
                        status=status.HTTP_202_ACCEPTED)
