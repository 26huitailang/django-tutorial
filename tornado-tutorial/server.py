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
from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler
from tornado.web import gen

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 引入django的配置
sys.path.append(BASE_DIR + '/mysite/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()
from rest_framework.renderers import JSONRenderer
from mzitu.models.tag import Tag
from mzitu.models.downloaded_suite import DownloadedSuite
from mzitu.serializers import MzituDownloadedSuiteSerializer
from mzitu.runtimes.suite import get_local_suite_count

# sql_file = os.path.join(BASE_DIR, 'mysite', 'mysite', 'local.sqlite3')
# print(sql_file)
# connection = sqlite3.connect(sql_file)
# c = connection.cursor()

define("port", default=8001, type=int)


# class PotatoCart(object):
#     total = 10
#     callbacks = []
#     carts = {}  # 购物车
#
#     def register(self, callback):
#         print(callback)
#         self.callbacks.append(callback)
#
#     def unregister(self, callback):
#         self.callbacks.remove(callback)
#
#     def move_item_to_cart(self, session):
#         if session in self.carts:
#             return
#
#         self.carts[session] = True
#         self.notify_callbacks()
#
#     def remove_item_from_cart(self, session):
#         if session not in self.carts:
#             return
#
#         del (self.carts[session])
#         self.notify_callbacks()
#
#     def notify_callbacks(self):
#         for callback in self.callbacks:
#             callback(self.get_inventory_count())
#
#     def get_inventory_count(self):
#         return self.total - len(self.carts)


class WebSocketHandler(WebSocketHandler):
    users = set()  # 用来存放在线用户的容器

    async def open(self):
        # self.users.add(self)  # 建立连接后添加用户到容器中
        print("{} 连接".format(self.get_query_argument('username')))
        print("{}".format(self.get_query_argument('suite_id')))
        # self.application.potato_cart.register(self.callback)
        # for u in self.users:  # 向已在线用户发送消息
        #     u.write_message(
        #         u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        # c.execute('select * from mzitu_tag limit 1')
        # tag = c.fetchone()
        # print(tag)
        # print(Tag.objects.first())
        # todo: auth
        await self.callback_downloadedsuite(self.get_query_argument('suite_id'))
        return

    async def on_message(self, message):
        # for u in self.users:  # 向在线用户广播消息
        #     u.write_message(u"[%s]-[%s]-说：%s" % (
        #     self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))
        # count = 0
        # while True:
        #     count += 1
        #     self.write_message("Back: {} {}".format(message, count))
        #     asyncio.sleep(5)
        # username = self.get_query_argument('username')
        # if message == 'add':
        #     self.application.potato_cart.move_item_to_cart(username)
        # elif message == 'remove':
        #     self.application.potato_cart.remove_item_from_cart(username)
        # tornado.ioloop.IOLoop.current().spawn_callback(self.callback_while, message)
        await self.callback_while(message)
        return

    def on_close(self):
        # self.users.remove(self)  # 用户关闭连接后从容器中移除用户
        # for u in self.users:
        #     u.write_message(
        #         u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print("close {}".format(self.close_reason))
        # self.application.potato_cart.unregister(self.callback)
        pass

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
        serializer = MzituDownloadedSuiteSerializer(suite)
        message = JSONRenderer().render(serializer.data)
        print(message)
        while True:
            local_files_count = get_local_suite_count(suite.name)
            # print(suite.max_page, suite.name, local_files_count)

            if last_local_files_count != local_files_count:
                # 两次检查到数据不一样的时候发送
                await self.write_message(message)
            await gen.sleep(1)
            last_local_files_count = local_files_count

            # if suite.max_page == local_files_count:
            #     break
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
    http_server.listen(options.port)
    http_server.start()
    tornado.ioloop.IOLoop.current().start()
