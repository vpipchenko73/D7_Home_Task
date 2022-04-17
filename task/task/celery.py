import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task.settings')
app = Celery('task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'weekly_newsletter': {
        'task': 'news.tasks.weekly_newsletter',
        'schedule': crontab( hour=8, minute=0, day_of_week='monday' ), # раасылка по понедельникам в 8.00

    },
}