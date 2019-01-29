# coding: utf-8

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from mzitu.models.proxy_ip import ProxyIp
from mzitu.models.tag import Tag
from mzitu.serializers import MzituDownloadedSuiteSerializer, TagSerializer

from django_vises.runtimes.misc import sort_dict_list


class ChartViewSet(GenericViewSet):
    serializer_class = MzituDownloadedSuiteSerializer
    queryset = ProxyIp.objects

    @action(methods=['GET'], detail=False)
    def tags_bar(self, request):
        tag_objs = Tag.objects.all()
        serializer_data = TagSerializer(tag_objs, many=True).data
        serializer_data_order_by_suites_count = sort_dict_list(serializer_data, 'suites_count')
        title = 'Tags统计'
        data = [x['suites_count'] for x in serializer_data_order_by_suites_count]
        response = {
            'title': title,
            'axisLabel': [x['name'] for x in serializer_data_order_by_suites_count],
            'data': data,
            'maxCount': max(data) if data else 0
        }

        return Response(response, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def proxyips_bar(self, request):
        query_data = ProxyIp.group_by_score()
        title = 'ProxyIp score统计'
        count_list = [x[1] for x in query_data]
        response = {
            'title': title,
            'data': query_data,
            'maxCount': max(count_list) if count_list else 0
        }
        return Response(response, status=status.HTTP_200_OK)
