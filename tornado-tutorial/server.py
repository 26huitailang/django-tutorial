# coding=utf-8

# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import sqlite3
import datetime

from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler

define("port", default=8001, type=int)

file = os.path.join(os.path.dirname(__file__), 'local.sqlite3')
print(file)
# connection = sqlite3.connect('mysite/mysite/local.sqlite3')
# c = connection.cursor()


class WebSocketHandler(WebSocketHandler):
    # users = set()  # 用来存放在线用户的容器

    def open(self):
        # self.users.add(self)  # 建立连接后添加用户到容器中
        # for u in self.users:  # 向已在线用户发送消息
        #     u.write_message(
        #         u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        # c.execute('select * from mzitu_tag limit 1')
        # tag = c.fetchone()
        # print(tag)
        pass

    def on_message(self, message):
        # for u in self.users:  # 向在线用户广播消息
        #     u.write_message(u"[%s]-[%s]-说：%s" % (
        #     self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))
        self.write_message("Back: {}".format(message))

    def on_close(self):
        # self.users.remove(self)  # 用户关闭连接后从容器中移除用户
        # for u in self.users:
        #     u.write_message(
        #         u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print("close {}".format(self))
        pass

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        # (r"/", IndexHandler),
        # (r"/chat", ChatHandler),
        (r"/ws", WebSocketHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
