from influxdb import InfluxDBClient
from django.conf import settings


def init_influxdb_client(
    host=settings.INFLUXDB_CONF['HOST'],
    port=settings.INFLUXDB_CONF['PORT'],
    username=settings.INFLUXDB_CONF['USERNAME'],
    password=settings.INFLUXDB_CONF['PASSWORD'],
    database=settings.INFLUXDB_CONF['DATABASE'],
    timeout=settings.INFLUXDB_CONF['TIMEOUT'],
):
    client = InfluxDBClient(
        host=host,
        port=port,
        username=username,
        password=password,
        database=database,
        timeout=timeout,
    )

    return client

def influxdb_query(sql, client):
    result = client.query(sql)

    return result