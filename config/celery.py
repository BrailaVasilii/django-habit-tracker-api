import os
from celery import Celery
from celery.schedules import crontab

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('habit_tracker')

# Load config from Django settings (cu prefix CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks din toate apps Django
app.autodiscover_tasks()

# Configurare Celery Beat schedule
app.conf.beat_schedule = {
    'send-habit-reminders-every-hour': {
        'task': 'habits.tasks.send_habit_reminders',
        'schedule': crontab(minute=0),  # La fiecare oră
    },
}

app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    """Debug task pentru testing Celery"""
    print(f'Request: {self.request!r}')