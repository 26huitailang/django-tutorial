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
    def test(self, request):
        """获取新的proxy ip"""
        tag_objs = Tag.objects.all()
        serializer_data = TagSerializer(tag_objs, many=True).data
        serializer_data_order_by_suites_count = sort_dict_list(serializer_data, 'suites_count', reverse=True)
        title = 'Tags统计'
        # x_axis =
        response = {
            'title': {
                'text': title
            },
            'legend': {
                'data': ['bar']
            },
            'tooltip': {
            },
            'xAxis': {
                'name': 'TagName',
                'data': [x['name'] for x in serializer_data_order_by_suites_count],
                'nameRotate': 30,
            },
            'yAxis': {},
            'series': [
                {
                    # // cozordinateSystem: 'polar',
                    'name': 'line',
                    'type': 'bar',
                    'showSymbol': False,
                    'data': [x['suites_count'] for x in serializer_data_order_by_suites_count]
                }
            ],
            'animationDuration': 2000
        }

        return Response(response, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'])
    # def check_valid(self, request):
    #     """标记失效的代理"""
    #     return
