import os
from celery import Celery
import django
from .config import CeleryConfig

__all__ = ['app']


class MyCelery(Celery):
    def now(self):
        from datetime import datetime
        return datetime.now(self.timezone)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_test.settings')
django.setup()
app = MyCelery('test')
app.config_from_object(CeleryConfig)
app.autodiscover_tasks()
