from django.shortcuts import render
from django.http import JsonResponse
from influxdb_plotly.runtimes.influxdb import (
    init_influxdb_client,
    influxdb_query,
)
import plotly
import plotly.graph_objs as go


def index(request):

    return render(request=request, template_name="influxdb_plotly/index.html")


def stream_data(request):
    sql = "select sum(sum) from stream group by time(6h), region limit 10000"
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
    group_by_result = result.items()
    lines = []
    for k, points in group_by_result:
        points = list(points)
        x = [x['time'] for x in points]
        y = [y['sum'] for y in points]
        line = go.Scatter(
            x=x,
            y=y,
            mode='line',
            name=k[1]['region']
        )
        lines.append(line)

    # 这里会自动打开一个html文件，是绘制的图像
    # plotly.offline.plot(lines, filename='curves')

    # 作图的布局
    layout = {
        'title': "流量曲线",
        'xaxis': {
            'tickangle': 30,
            'tickformat': '%x',
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
