# coding: utf-8
from .base import *

DEBUG = True

DATABASES['default']['NAME'] = 'local.sqlite3'

IMAGE_FOLDER = '/tmp/mzitu'

RAVEN_CONFIG['dsn'] = None  # YOURS
