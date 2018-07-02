try:
    from .settings import *
except ImportError as e:
    from .base import *