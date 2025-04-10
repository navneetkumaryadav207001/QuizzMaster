from celery.schedules import crontab
from app import celery
from tasks import send_daily_reminders

celery.conf.beat_schedule = {
    "send-daily-reminders": {
        "task": "tasks.send_daily_reminders",
        "schedule": crontab(hour=19, minute=0),  # Runs every day at 7 PM
    },
}
