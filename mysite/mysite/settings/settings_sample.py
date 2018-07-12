# coding: utf-8
from .base import *

DEBUG = True

DATABASES['default']['NAME'] = 'local.sqlite3'

# Channels
ASGI_APPLICATION = 'mysite.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)]
        }
    }
}
