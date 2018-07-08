#!/usr/bin/python
# coding: utf-8


from mzitu.models import ProxyIp


# def get_conn(path=DB_PATH, db_name=DB_NAME):
#     db_url = os.path.join(path, db_name)
#     conn = sqlite3.connect(db_url)
#
#     return conn


# def create_table():
#     conn = get_conn()
#     cursor = conn.cursor()
#     cursor.execute(
#         'create table proxy_ip (id INTEGER PRIMARY KEY AUTOINCREMENT, ip varchar(16), port varchar(16), is_valid integer(1))'
#     )
#     cursor.close()


def get_proxy_ip_valid():
    # conn = get_conn()
    # cursor = conn.cursor()
    # cursor.execute('SELECT ip, port from mzitu_proxyip WHERE is_valid=?', (1,))
    # results = cursor.fetchall()
    # cursor.close()
    item = ProxyIp.objects.filter(is_valid=1).first()

    return item


def mark_proxy_ip_not_valid(ip, port):
    # conn = get_conn()
    # cursor = conn.cursor()
    # cursor.execute('UPDATE proxy_ip SET is_valid = 0 WHERE ip=? AND port=?;', (ip, port))
    # conn.commit()
    # conn.close()
    item = ProxyIp.objects.filter(ip=ip, port=port).first()
    if item:
        item.is_valid = 0
        item.save()


def insert_proxy_ip(ip, port, is_valid=1):
    item = ProxyIp.objects.filter(ip=ip, port=port).first()
    if not item:
        item = ProxyIp(ip=ip, port=port, is_valid=is_valid)
        item.save()
