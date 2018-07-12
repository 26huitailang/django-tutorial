#!/usr/bin/env python
# coding=utf-8
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    """Asynchronous ChatConsumer"""
    async def connect(self):
        """
        Every consumer has a scope that contains information about its
        connection, including in particular any positional or keyword
        arguments from the URL route and the currently authenticated user
        if any.
        """
        # room_name来自于url，见chat/routing.py
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # 通过用户指定的room_name构建Channels group name
        # 这里没有做字符串检查，所以一般只允许包含字符、数字、连接符、句号，其他可能会失败
        self.room_group_name = 'chat_{}'.format(self.room_name)

        # Join room group
        """
        The async_to_sync(…) wrapper is required because ChatConsumer is a
         synchronous WebsocketConsumer but it is calling an asynchronous
          channel layer method. (All channel layer methods are asynchronous.)
        """
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # 接收WebSocket连接
        # 如果不在connect这个方法中调用accept()那么这个连接会被拒绝和关闭
        # 可以在这里认证用户，如果没有通过认证，就不调用accept关闭连接
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """Receive message from WebSocket"""

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        # 其实是发送一个message标记的event到group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # 用来让consumers识别event的
                'message': message,
            }
        )

    async def chat_message(self, event):
        """Receive message from room group"""
        # 和上面发送到group的event type 有关
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


# class ChatConsumer(WebsocketConsumer):
#     """synchronous ChatConsumer"""
#     def connect(self):
#         """
#         Every consumer has a scope that contains information about its
#         connection, including in particular any positional or keyword
#         arguments from the URL route and the currently authenticated user
#         if any.
#         """
#         # room_name来自于url，见chat/routing.py
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         # 通过用户指定的room_name构建Channels group name
#         # 这里没有做字符串检查，所以一般只允许包含字符、数字、连接符、句号，其他可能会失败
#         self.room_group_name = 'chat_{}'.format(self.room_name)
#
#         # Join room group
#         """
#         The async_to_sync(…) wrapper is required because ChatConsumer is a
#          synchronous WebsocketConsumer but it is calling an asynchronous
#           channel layer method. (All channel layer methods are asynchronous.)
#         """
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         # 接收WebSocket连接
#         # 如果不在connect这个方法中调用accept()那么这个连接会被拒绝和关闭
#         # 可以在这里认证用户，如果没有通过认证，就不调用accept关闭连接
#         self.accept()
#
#     def disconnect(self, code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     def receive(self, text_data=None, bytes_data=None):
#         """Receive message from WebSocket"""
#
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # Send message to room group
#         # 其实是发送一个message标记的event到group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',  # 用来让consumers识别event的
#                 'message': message,
#             }
#         )
#
#     def chat_message(self, event):
#         """Receive message from room group"""
#         # 和上面发送到group的event type 有关
#         message = event['message']
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))
