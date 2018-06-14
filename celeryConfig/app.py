import os
from celery import Celery
import django
from .config import CeleryConfig

__all__ = ['app']


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_test.settings')
django.setup()
app = Celery('test')
app.config_from_object(CeleryConfig)
app.autodiscover_tasks()
