from django.core.management import BaseCommand
import random
import time
import datetime
from influxdb_plotly.runtimes.influxdb import (
    init_influxdb_client,
)


class Command(BaseCommand):

    host_list = [
        ('1.1.1.1', 'HK'),
        ('2.2.2.2', 'JP'),
        ('3.3.3.3', 'KR'),
        ('4.4.4.4', 'USA'),
    ]
    measurement = 'stream'
    STREAM_MIN = 0
    STREAM_MAX = 10000  # MB
    influxdb_dbname = 'test_plotly'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            action='store',
            dest='days',
            default=30,
            type=int,
            help='随机插入的时间段，往前多少天',
        )

        parser.add_argument(
            '--num',
            action='store',
            dest='num',
            default=10000,
            type=int,
            help='共插入多少个点'
        )

        parser.add_argument(
            '--drop',
            action='store_true',
            dest='drop',
            default=False,
            # type=bool,
            help='是否删除之前的点'
        )

    def handle(self, *args, **options):
        num_of_points = options['num']
        days = options['days']
        drop = options['drop']

        # 随机的时间戳起止
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        start_ts = int(start_date.timestamp()) * 10 ** 9  # influxdb的时间戳比int(time.time())多了9位
        end_ts = int(end_date.timestamp()) * 10 ** 9

        client = init_influxdb_client(database=self.influxdb_dbname)
        if drop:
            client.query("drop measurement {}".format(self.measurement))
        
        json_body = []
        for i in range(num_of_points):
            upload = random.randint(self.STREAM_MIN, self.STREAM_MAX + 1)
            download = random.randint(self.STREAM_MIN, self.STREAM_MAX + 1)
            host = random.choice(self.host_list)
            point = {
                "measurement": self.measurement,
                "tags": {
                    "host": host[0],
                    "region": host[1],
                },
                "time": random.randint(start_ts, end_ts),  # random timestamp
                "fields": {
                    "upload": upload,
                    "download": download,
                    "sum": upload + download,
                }
            }
            json_body.append(point)
            if i % 10000 == 0:
                client.write_points(json_body)
                json_body.clear()

        client.write_points(json_body)
