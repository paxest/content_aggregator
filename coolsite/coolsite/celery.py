from __future__ import absolute_import
import os
from celery import Celery

from celery.schedules import crontab # scheduler

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
# default django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coolsite.settings')
app = Celery('coolsite')
app.conf.timezone = 'UTC'
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # executes every 1 minute
    'scraping-task-one-min': {
        'task': 'content_aggregator.tasks.interfax_parser',
        'schedule': crontab(),
    },
    # # executes every 15 minutes
    # 'scraping-task-fifteen-min': {
    #     'task': 'tasks.hackernews_rss',
    #     'schedule': crontab(minute='*/15')
    # },
    # # executes daily at midnight
    # 'scraping-task-midnight-daily': {
    #     'task': 'tasks.hackernews_rss',
    #     'schedule': crontab(minute=0, hour=0)
    # }
}