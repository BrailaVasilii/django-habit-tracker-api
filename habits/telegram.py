import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id: str, message: str) -> bool:
    """
    Trimite mesaj către user prin Telegram Bot.

    Args:
        chat_id: Telegram chat ID al user-ului
        message: Mesajul de trimis

    Returns:
        bool: True dacă mesajul a fost trimis cu succes, False altfel
    """
    if not chat_id:
        logger.warning("Chat ID is empty, cannot send message")
        return False

    bot_token = settings.TELEGRAM_BOT_TOKEN

    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not configured in settings")
        return False

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()

        result = response.json()

        if result.get('ok'):
            logger.info(f"Message sent successfully to chat_id: {chat_id}")
            return True
        else:
            logger.error(f"Telegram API error: {result}")
            return False

    except requests.RequestException as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


def format_habit_reminder(habit) -> str:
    """
    Formatează mesajul de reminder pentru un habit.

    Args:
        habit: Obiect Habit

    Returns:
        str: Mesaj formatat pentru Telegram
    """
    message = f"🔔 <b>Reminder: Time for your habit!</b>\n\n"
    message += f"📝 <b>Action:</b> {habit.action}\n"
    message += f"📍 <b>Place:</b> {habit.place}\n"
    message += f"⏰ <b>Time:</b> {habit.time.strftime('%H:%M')}\n"
    message += f"⏱ <b>Duration:</b> {habit.duration} seconds\n"

    if habit.reward:
        message += f"🎁 <b>Reward:</b> {habit.reward}\n"
    elif habit.related_habit:
        message += f"😊 <b>Pleasant habit:</b> {habit.related_habit.action}\n"

    message += f"\n💪 You can do it!"

    return message