from django.shortcuts import render
from django.http import JsonResponse
from influxdb_plotly.runtimes.influxdb import (
    init_influxdb_client,
    influxdb_query,
)


def stream_data(request):
    sql = "select * from stream"
    # client = init_influxdb_client()
    # result = influxdb_query(sql, client)

    result = {
        '1': 'aaa',
        '2': '23',
        '3': {
            '4': '456',
        }
    }
    return JsonResponse(result)
