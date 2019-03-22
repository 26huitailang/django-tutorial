"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import raven
import datetime
from celery.schedules import crontab
from mysite.deploy_level import DeployLevel

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vnimhx9&@_bwm!j7fptet%+wba20@nc=fwu*khw0^)g3%0w_01'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DEPLOY_LEVEL = DeployLevel.develop
is_docker = os.environ.get('DOCKER')

# CSRF_COOKIE_SECURE = False
ALLOWED_HOSTS = []


# todo: 已建分支备份，删除不用的app和依赖
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'raven.contrib.django.raven_compat',  # sentry
    'drf_yasg',  # api docs
    # 'channels',  # websocket
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'mzitu',
    'polls',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': ['frontend/dist'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'local.sqlite3'),
    #     # When using the SQLite database engine the Django tests will by default use an in-memory database.
    #     'TEST': {
    #         'NAME': 'testdb.sqlite3',
    #     }
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_tutorial',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'db' if is_docker else 'localhost',
        'PORT': 5432 if is_docker else 10864,
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'running', 'cdn', 'static')

# Add for Vue
STATICFILES_DIRS = [
    os.path.join(os.path.dirname(BASE_DIR), 'frontend/dist/static'),
    os.path.join(os.path.dirname(BASE_DIR), 'frontend/dist'),  # icon
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    # 'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
# USE_SESSION_AUTH = True
LOGIN_URL = '/api/v1/auth/login/'
LOGOUT_URL = '/api/v1/auth/logout/'

# Sessions
SESSION_COOKIE_AGE = 43200

# corsheaders 跨域
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '*'
)
# CORS_ALLOW_METHODS = (
#     # 'DELETE',
#     'GET',
#     # 'OPTIONS',
#     # 'PATCH',
#     'POST',
#     # 'PUT',
# )
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# redis for docker
REDIS_HOST = 'redis' if is_docker else 'localhost'

# ------------------------------------------------------------
# celery

# broker
if is_docker:
    CELERY_BROKER_URL = 'redis://redis:6379/0'
else:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'

# timezone
CELERY_TIMEZONE = 'Asia/Shanghai'

# todo: 这种管理不优雅
CELERY_BEAT_SCHEDULE = {
    # timedelta ------------------------------------------------------------
    'check-proxy-ip-per-5-minute': {
        # 检查任务
        'task': 'mzitu.tasks.proxy_ip.check_proxy_ip',
        'schedule': datetime.timedelta(minutes=5),
    },
    'get-proxy-ip-and-delete-invalid-per-6-hour': {
        # 获得新代理ip，删除失效代理ip
        'task': 'mzitu.tasks.proxy_ip.get_proxy_ips_crontab',
        # 'schedule': crontab(hour='*/2'),
        'schedule': datetime.timedelta(hours=2),
    },
    # crontab ------------------------------------------------------------
    'delete-invalid-local-imgs-every-day-0-clock': {
        # 删除数据库中没有记录的本地文件
        'task': 'mzitu.tasks.local_imgs.delete_imgs',
        'schedule': crontab(minute='0', hour='22'),  # 每晚22点
    }
}
# 限制任务的速率，这样每分钟只允许处理 12 个该类型的任务
# CELERY_TASK_DEFAULT_RATE_LIMIT = '60/m'  # 5 seconds interval time between tow tasks
CELERY_TASK_ANNOTATIONS = {
    'mzitu.tasks.proxy_ip.check_proxy_ip': {'rate_limit': '2/m'},
    # 'mzitu.tasks.proxy_ip.get_proxy_ips_crontab': {'rate_limit': '1/h'},  # todo: celery4.2.1会导致所有的间隔都变为1hour
}

# 获取proxy_ip 的地方
PROXY_SOURCE_URL = 'http://www.xicidaili.com/nn/'

MEDIA_URL = '/media/'
home_path = os.environ.get('HOME')
MEDIA_ROOT = os.path.join(home_path, 'Downloads')
IMAGE_FOLDER_MZITU = os.path.join(MEDIA_ROOT, 'mzitu')
IMAGE_FOLDER_MEITURI = os.path.join(MEDIA_ROOT, 'meituri')

# ------------------------------------------------------------
# Sentry
RAVEN_CONFIG = {
    'dsn': None,
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))),
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志文件地址
            'filename': os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'logs', 'server.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'default',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
    },
    'filters': {  # 日志过滤器
        'require_debug_true': {  # 是否支持DEBUG级别日志过滤
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', ],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'mzitu': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
        },
    },
}
