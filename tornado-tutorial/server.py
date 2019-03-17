# coding=utf-8
"""
怎么实现我要的效果，发送重下载指令之后，建立ws来获取后端进度的变化

注册的callback函数写为while？会阻塞吗？
"""
import os
import sys
import sqlite3
import asyncio
import datetime
import time
import django

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
# from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler
from tornado.web import gen

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 引入django的配置
sys.path.append(BASE_DIR + '/mysite/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()
from rest_framework.renderers import JSONRenderer
# from mzitu.models.tag import Tag
from mzitu.models.downloaded_suite import DownloadedSuite
from mzitu.serializers import MzituDownloadedSuiteSerializer
from mzitu.runtimes.mzitu_suite import get_local_suite_count
from rest_framework.authtoken.models import Token

# sql_file = os.path.join(BASE_DIR, 'mysite', 'mysite', 'local.sqlite3')
# print(sql_file)
# connection = sqlite3.connect(sql_file)
# c = connection.cursor()

define("port", default=8010, type=int)


def user_auth(key):
    """简单固定token认证"""
    if not key:
        return False

    token = Token.objects.filter(key=key).first()
    if token is None:
        return False

    return True


class WebSocketHandler(WebSocketHandler):
    users = set()  # 用来存放在线用户的容器

    async def open(self):
        # self.users.add(self)  # 建立连接后添加用户到容器中
        # 利用这个自定义的header来存token，标准建议用于协议或域名
        if not user_auth(self.request.headers.get('Sec-WebSocket-Protocol', None)):
            self.write_message('用户认证失败')
        else:
            print("{} 连接".format(self.get_query_argument('username')))
            print("{}".format(self.get_query_argument('suite_id')))
            asyncio.ensure_future(self.callback_downloadedsuite(self.get_query_argument('suite_id')))

    async def on_message(self, message):
        asyncio.ensure_future(self.callback_while(message))

    def on_close(self):
        # self.users.remove(self)  # 用户关闭连接后从容器中移除用户
        print("close {}".format(self.close_reason))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

    def callback(self, count):
        self.write_message(f'inventoryCount: {count}')

    async def callback_while(self, message):
        count = 0
        while True:
            count += 1
            await self.write_message("Back: {} {} {}".format(datetime.datetime.now(), message, count))
            await gen.sleep(5)

    async def callback_downloadedsuite(self, suite_id):
        suite = DownloadedSuite.objects.filter(id=suite_id).first()
        last_local_files_count = 0
        while True:
            local_files_count = get_local_suite_count(suite.name)
            # print(suite.max_page, suite.name, local_files_count)

            print(last_local_files_count, local_files_count)
            if last_local_files_count != local_files_count:
                # 两次检查到数据不一样的时候发送
                serializer = MzituDownloadedSuiteSerializer(suite)
                message = JSONRenderer().render(serializer.data)
                await self.write_message(message)
            await gen.sleep(1)
            last_local_files_count = local_files_count

            if suite.max_page == local_files_count:
                break
        self.close(reason='下载完成')  # 关闭这次连接
        return


class Application(tornado.web.Application):
    def __init__(self):
        # self.potato_cart = PotatoCart()

        handlers = [
            # (r"/", IndexHandler),
            # (r"/chat", ChatHandler),
            (r"/ws", WebSocketHandler),
        ]

        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            debug=True
        )

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, address='0.0.0.0')
    http_server.start()
    tornado.ioloop.IOLoop.current().start()
