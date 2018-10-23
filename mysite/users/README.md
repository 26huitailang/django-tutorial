# users app

用于模拟一些前后端分离的登陆/认证方式，希望看到的朋友有所帮助。

- [django-rest-framework-jwt](https://github.com/GetBlimp/django-rest-framework-jwt)
- django.contrib.auth 模块的session authentication

## swagger

`127.0.0.1:8000`

session认证才能使用的功能在右上角登录后可见，登录的过程是设置sessionid和csrftoken的过程。

## 功能

- [ ] JWT: 以API的形式提供JWT的登陆方式
  - authtoken
  - refreshtoken
- [x] django.contrib.auth 模块的session authentication
  - session/cookie/csrftoken
  - session是在服务端保存，可以设置登录返回的`sessionid`给浏览器
  - cookie，每次浏览器访问携带的内容，将sessionid存在这里
  - csrftoken设置在cookie里面，前端的请求需要将这个value放入`header`中的`x-csrftoken`，在get以外的请求需要这个header
