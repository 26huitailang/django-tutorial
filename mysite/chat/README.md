# chat

django集成websocket的应用。

## channels

- 在INSTALLED_APPS加入channels后，channels development server会替代django develop server，可能会造成冲突。`Starting ASGI/Channels version 2.1.2 development server at http://0:8001/`
- websocket 的wsURL最好以`/ws/`开头，以区别通常的http连接，也利于nginx反向代理时候将不同的服务发给不同的应用
- channel layer: is a kind of communication system. It allows multiple consumer instances to talk with each other, and with other parts of Django.
  - a channel: is a mailbox where messages can be sent to. Each channel has a name. Anyone who has the name of a channel can send a message to the channel.
  - 每个consumer instance都会自动生成一个独立的channel name，这样便可以通过channel layer与其他交流。
  - 多人聊天实际就是将多个ChatConsumer的channel添加到一个group里面（也就是room name）
  - a group: is a group of related channels. A group has a name. Anyone who has the name of a group can add/remove a channel to the group by name and send a message to all channels in the group. It is not possible to enumerate what channels are in a particular group.
  - 利用redis作为channel layer的后端存储

消息怎么走的：

- 用户post一个message，JS会通过WebSocket发送到一个ChatConsumer
- ChatConsumer收到消息，根据room name发送给group
- 每个在这个group的ChatConsumer都会收到消息
- ChatConsumer再通过WebSocket返回消息给JS，就会显示在大家的屏幕上了，这里也就体现了WebSocket双向的工作方式了
