# influxdb_plotly

## change-log

- 2018-07-04，试试用drf写api

## 说明

写这个app是为了测试一个看板方案的组合：

- Django，提供后端的服务
- influxdb，提供用于作图数据的时序数据库
- 其他SQL数据库，本身运营中的数据库，一些管理类数据，走connection的方式通过SQL查询，因为Grafana也是用SQL维护的。
