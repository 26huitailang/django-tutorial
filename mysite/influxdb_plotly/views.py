from django.shortcuts import render
from django.http import JsonResponse
from influxdb_plotly.runtimes.influxdb import (
    init_influxdb_client,
    influxdb_query,
)
import plotly.graph_objs as go
import datetime

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from influxdb_plotly.serializers.list_dict_serializer import ListDictSerializer


def index(request):

    return render(
        request=request,
        template_name="influxdb_plotly/index.html",
        context={'loop': list(range(2))}
    )


def stream_data(request):
    sql = "select sum(sum) from stream group by time(1d), region"
    # sql = "select sum(sum) from stream group by time(6h), region limit 100"
    client = init_influxdb_client()
    result = influxdb_query(sql, client)
    # print(result)
    # points = list(result.get_points())

    """单线"""
    # plotly.offline.plot({
    #     "data": [go.Scatter(x=[x['time'] for x in points], y=[y['sum'] for y in points])],
    #     "layout": go.Layout(title="hello world")
    # }, auto_open=True)

    """多条曲线"""
    # 2018-04-03T08:52:56.389384262Z
    group_by_result = result.items()
    lines = []
    x_start = None
    x_end = None
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    for k, points in group_by_result:
        points = list(points)
        x = [x['time'] for x in points]
        # print(x[0], type(x[0]))
        if x_start:
            x_first = datetime.datetime.strptime(x[0], fmt)
            x_last = datetime.datetime.strptime(x[-1], fmt)
            if x_first < x_start:
                x_start = x_first
            if x_last > x_end:
                x_end = x_last
        else:
            x_start = datetime.datetime.strptime(x[0], fmt)
            x_end = datetime.datetime.strptime(x[-1], fmt)

        y = [y['sum'] for y in points]
        line = go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            name=k[1]['region']
        )
        lines.append(line)

    # 这里会自动打开一个html文件，是绘制的图像
    # plotly.offline.plot(lines, filename='curves')

    # 作图的布局
    # range_list = [x_start, x_end]
    layout = {
        'title': "流量曲线",
        'xaxis': {
            'tickangle': 30,
            'tickformat': '%y',
            # 'range': range_list,
        },
        'yaxis': {
            'title': '流量 GB',
            'titlefont': {
                'family': 'Courier New, monospace',
                'size': 12,
            },
        },
    }

    # plotly 的一些设置
    PLOTLY_SETTINGS_WITHOUT_TOOLBAR = {
        'displayModeBar': True,
        'modeBarButtonsToRemove': [
            'sendDataToCloud', 'pan2d', 'autoScale2d', 'hoverClosestCartesian', 'zoom2d',
            'hoverCompareCartesian', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d'],
        'displaylogo': False,
    }

    fig = {
        'data': lines,
        'layout': layout,
        'settings': PLOTLY_SETTINGS_WITHOUT_TOOLBAR,
    }

    """如果想在前端作图，就用plotly.js的库，然后用api返回前端需要的格式就行"""
    return JsonResponse({
        'is_success': True,
        'data': fig,
        'message': 'suuuuuuu'
    })


class ListDictViewSet(GenericViewSet):
    serializer_class = ListDictSerializer

    def get_queryset(self):
        sql = "select sum(sum) from stream group by time(1d), region"
        # sql = "select sum(sum) from stream group by time(6h), region limit 100"
        client = init_influxdb_client()
        result = influxdb_query(sql, client)
        return result

    def get_request_param_data(self):
        if self.request.method == 'GET':
            request_param_data = self.request.query_params
        else:
            request_param_data = self.request.data

        return request_param_data

    @action(detail=True, methods=['GET'])
    # check token
    def list_stream_points_order_by_time(self, request):
        request_param_data = self.get_request_param_data()
        print(request_param_data)

        # queryset = self.get_queryset()
