import os
from celery import Celery
from celery.schedules import crontab
from apis import get_news_from_query
from loguru import logger
from decouple import config
from django.conf import settings
from django.core.exceptions import ValidationError
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_scrapper.settings')
django.setup()

from tasks import get_news
from telegram_bot import send_news_to_users


app = Celery('news_scrapper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        # crontab(config('SEARCH_PERIOD_HOURS', cast=str, default='*/1')), # defaults to every hour
        crontab(minute='*/5'),
        task_get_news.s(),
    )

@app.task
def task_get_news():
    news = get_news()
    send_news_to_users(news)
    
