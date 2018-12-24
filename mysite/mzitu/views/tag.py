# coding: utf-8

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from mzitu.models.tag import Tag
from mzitu.serializers import TagSerailizer
from mzitu.runtimes.theme import get_suite_urls_to_redis
from mzitu.tasks.suite import download_one_suite


class TagViewSet(GenericViewSet):
    serializer_class = TagSerailizer
    queryset = Tag.objects.all()

    def list(self, request):
        """tag list"""
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like_toggle(self, request, pk: str = None):
        """标记like"""
        instance = get_object_or_404(Tag, id=pk)
        instance.is_like = not instance.is_like
        instance.save()
        return Response({ 'name': instance.name, 'is_like': instance.is_like},
                        status=status.HTTP_202_ACCEPTED)
