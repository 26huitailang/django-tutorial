from django.core.management import BaseCommand
import random
import time
import datetime
from influxdb_plotly.runtimes.influxdb import (
    init_influxdb_client,
)

class Commad(BaseCommand):

    NUM_OF_POINTS = 10000
    host_list = [
        ('1.1.1.1', 'HK'),
        ('2.2.2.2', 'JP'),
        ('3.3.3.3', 'KR'),
        ('4.4.4.4', 'USA'),
    ]
    measurement = 'stream'
    STREAM_MIN = 0,
    STREAM_MAX = 1000,  # MB
    influxdb_dbname = 'test_ploty'

    # 生成随机日期
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=30)
    start_ts = int(start_date.timestamp)
    end_ts = int(end_date.timestamp)

    def add_arguments(self, parser):

        parser.add_argument(
            '-n',
            '--name',
            action='store',
            dest='name',
            default='close',
            help='name of author.',
        )

    def handle(self, *args, **options):
        client = init_influxdb_client(database=self.influxdb_dbname)
        json_body = []
        for _ in range(self.NUM_OF_POINTS):
            upload = random.randint(self.STREAM_MIN, self.STREAM_MAX)
            download = random.randint(self.STREAM_MIN, self.STREAM_MAX)
            point = {
                "measurement": self.measurement,
                "tags": {
                    "host": random.choice(self.host_list[0]),
                    "region": random.choice(self.host_list[1]),
                },
                "time": random.randint(self.start_ts, self.end_ts),  # random timestamp
                "fields": {
                    "upload": upload,
                    "download": download,
                    "sum": upload + download,
                }
            }
            json_body.append(point)
        
        client.write_points(json_body)
