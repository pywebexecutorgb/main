import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'executor.settings')

app = Celery('executor')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clean-containers-every-2-minutes': {
        'task': 'mainapp.tasks.clean_containers',
        'schedule': 120.0,
        'args': (),
    },
}
