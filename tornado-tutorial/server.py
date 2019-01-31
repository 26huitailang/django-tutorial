# coding=utf-8
"""
怎么实现我要的效果，发送重下载指令之后，建立ws来获取后端进度的变化

注册的callback函数写为while？会阻塞吗？
"""
import os
import sys
import sqlite3
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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR + '/mysite/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()
from mzitu.models.tag import Tag

# sql_file = os.path.join(BASE_DIR, 'mysite', 'mysite', 'local.sqlite3')
# print(sql_file)
# connection = sqlite3.connect(sql_file)
# c = connection.cursor()

define("port", default=8001, type=int)


class PotatoCart(object):
    total = 10
    callbacks = []
    carts = {}  # 购物车

    def register(self, callback):
        print(callback)
        self.callbacks.append(callback)

    def unregister(self, callback):
        self.callbacks.remove(callback)

    def move_item_to_cart(self, session):
        if session in self.carts:
            return

        self.carts[session] = True
        self.notify_callbacks()

    def remove_item_from_cart(self, session):
        if session not in self.carts:
            return

        del (self.carts[session])
        self.notify_callbacks()

    def notify_callbacks(self):
        for callback in self.callbacks:
            callback(self.get_inventory_count())

    def get_inventory_count(self):
        return self.total - len(self.carts)


class WebSocketHandler(WebSocketHandler):
    users = set()  # 用来存放在线用户的容器

    def open(self):
        self.users.add(self)  # 建立连接后添加用户到容器中
        print("{} 加入".format(self.get_query_argument('username')))
        self.application.potato_cart.register(self.callback)
        # for u in self.users:  # 向已在线用户发送消息
        #     u.write_message(
        #         u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        # c.execute('select * from mzitu_tag limit 1')
        # tag = c.fetchone()
        # print(tag)
        # print(Tag.objects.first())
        pass

    def on_message(self, message):
        # for u in self.users:  # 向在线用户广播消息
        #     u.write_message(u"[%s]-[%s]-说：%s" % (
        #     self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))
        # count = 0
        # while True:
        #     count += 1
        #     self.write_message("Back: {} {}".format(message, count))
        #     time.sleep(5)
        username = self.get_query_argument('username')
        if message == 'add':
            self.application.potato_cart.move_item_to_cart(username)
        elif message == 'remove':
            self.application.potato_cart.remove_item_from_cart(username)


    def on_close(self):
        # self.users.remove(self)  # 用户关闭连接后从容器中移除用户
        # for u in self.users:
        #     u.write_message(
        #         u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print("close {}".format(self))
        self.application.potato_cart.unregister(self.callback)
        pass

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

    def callback(self, count):
        self.write_message(f'inventoryCount: {count}')


class Application(tornado.web.Application):
    def __init__(self):
        self.potato_cart = PotatoCart()

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
