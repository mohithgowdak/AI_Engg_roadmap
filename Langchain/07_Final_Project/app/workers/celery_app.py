from celery import Celery
from celery.schedules import crontab

from app.config import settings


celery_app = Celery("pricedrop", broker=settings.redis_url, backend=settings.redis_url)

celery_app.conf.beat_schedule = {
    "poll-amazon-every-3-hours": {
        "task": "app.workers.tasks.poll_prices_and_enqueue_alerts",
        "schedule": crontab(minute=0, hour="*/3"),
    },
    "send-pending-alerts-every-5-min": {
        "task": "app.workers.tasks.send_pending_alerts",
        "schedule": crontab(minute="*/5"),
    },
}

celery_app.conf.timezone = "UTC"
