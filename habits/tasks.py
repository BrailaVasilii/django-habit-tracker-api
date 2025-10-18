from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta
import logging
from .models import Habit
from .telegram import send_telegram_message, format_habit_reminder

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminder(habit_id: int) -> dict:
    """
    Trimite reminder pentru un habit specific.

    Args:
        habit_id: ID-ul habit-ului

    Returns:
        dict: Rezultatul operației cu status și detalii
    """
    try:
        habit = Habit.objects.select_related('user', 'related_habit').get(id=habit_id)
    except Habit.DoesNotExist:
        logger.error(f"Habit with id {habit_id} does not exist")
        return {
            'status': 'error',
            'habit_id': habit_id,
            'message': 'Habit not found'
        }

    # Verifică dacă user-ul are telegram_chat_id
    if not habit.user.telegram_chat_id:
        logger.info(f"User {habit.user.email} doesn't have Telegram chat ID")
        return {
            'status': 'skipped',
            'habit_id': habit_id,
            'message': 'User has no Telegram chat ID'
        }

    # Formatează și trimite mesajul
    message = format_habit_reminder(habit)
    success = send_telegram_message(habit.user.telegram_chat_id, message)

    if success:
        logger.info(f"Reminder sent for habit {habit_id}: {habit.action}")
        return {
            'status': 'success',
            'habit_id': habit_id,
            'message': f'Reminder sent for: {habit.action}'
        }
    else:
        logger.error(f"Failed to send reminder for habit {habit_id}")
        return {
            'status': 'error',
            'habit_id': habit_id,
            'message': 'Failed to send Telegram message'
        }


@shared_task
def send_habit_reminders() -> dict:
    """
    Verifică toate habits și trimite reminders pentru cele care trebuie executate.
    Rulează periodic prin Celery Beat.

    Returns:
        dict: Statistici despre reminders trimise
    """
    now = timezone.now()
    current_time = now.time()
    current_date = now.date()

    logger.info(f"Checking habits for reminders at {current_time}")

    # Găsește habits care trebuie executate acum
    # Verificăm habits cu timpul în următoarea oră
    time_window_start = (now - timedelta(minutes=30)).time()
    time_window_end = (now + timedelta(minutes=30)).time()

    habits = Habit.objects.filter(
        time__gte=time_window_start,
        time__lte=time_window_end,
        user__telegram_chat_id__isnull=False
    ).select_related('user', 'related_habit')

    sent_count = 0
    error_count = 0
    skipped_count = 0

    for habit in habits:
        # Verifică periodicitatea (simplificat pentru demonstrație)
        # În producție, ar trebui să trackuim când a fost trimis ultimul reminder

        result = send_habit_reminder.delay(habit.id)

        # Pentru testing, putem aștepta rezultatul
        # În producție, task-ul rulează async

        sent_count += 1

    logger.info(
        f"Reminders check complete: {sent_count} sent, "
        f"{error_count} errors, {skipped_count} skipped"
    )

    return {
        'status': 'complete',
        'sent': sent_count,
        'errors': error_count,
        'skipped': skipped_count,
        'checked_at': now.isoformat()
    }