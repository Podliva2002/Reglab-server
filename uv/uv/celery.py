from celery import Celery
import os
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uv.settings')

app = Celery('uv')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'subject': {
        'task': 'main.tasks.email',
        'schedule': crontab(hour=1, minute=30),
    },
}

