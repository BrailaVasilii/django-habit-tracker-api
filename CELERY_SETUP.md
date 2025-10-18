# Celery Setup și Comenzi

## Pornire Celery Worker
```bash
# În terminal separat (cu Poetry shell activ)
celery -A config worker -l info
```

## Pornire Celery Beat (Scheduler)
```bash
# În terminal separat (cu Poetry shell activ)
celery -A config beat -l info
```

## Pornire Worker + Beat împreună
```bash
celery -A config worker -l info --beat
```

## Test Manual Task
```python
# În Django shell
python manage.py shell

from habits.tasks import send_habit_reminder
from habits.models import Habit

# Trimite reminder pentru habit cu ID 1
result = send_habit_reminder.delay(1)
print(result.get())
```

## Monitoring Celery
```bash
# Flower - Celery monitoring tool (optional)
pip install flower
celery -A config flower
# Acces: http://localhost:5555
```

## Note

- Redis trebuie să ruleze pentru Celery
- Celery Beat trebuie să ruleze pentru scheduled tasks
- În producție, folosește process manager (Supervisor, systemd)