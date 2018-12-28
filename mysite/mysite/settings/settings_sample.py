# coding: utf-8
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES['default']['NAME'] = 'local.sqlite3'

IMAGE_FOLDER = '/tmp/mzitu'

RAVEN_CONFIG['dsn'] = None  # YOURS
