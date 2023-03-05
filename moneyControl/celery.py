import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneyControl.settings')

app = Celery('moneyControl')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

