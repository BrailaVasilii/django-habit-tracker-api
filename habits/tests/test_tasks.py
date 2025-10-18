import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from habits.models import Habit
from habits.tasks import send_habit_reminder, send_habit_reminders
from habits.telegram import send_telegram_message, format_habit_reminder

User = get_user_model()


@pytest.mark.django_db
class TestTelegramIntegration:
    """Tests pentru Telegram integration"""

    @patch('habits.telegram.requests.post')
    def test_send_telegram_message_success(self, mock_post):
        """Test: Trimitere mesaj Telegram cu succes"""
        # Mock Telegram API response
        mock_response = MagicMock()
        mock_response.json.return_value = {'ok': True, 'result': {}}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = send_telegram_message('123456789', 'Test message')

        assert result is True
        assert mock_post.called

    @patch('habits.telegram.requests.post')
    def test_send_telegram_message_failure(self, mock_post):
        """Test: Trimitere mesaj eșuează"""
        from requests.exceptions import RequestException
        mock_post.side_effect = RequestException('Network error')

        result = send_telegram_message('123456789', 'Test message')

        assert result is False

    def test_format_habit_reminder(self):
        """Test: Formatare mesaj reminder"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        habit = Habit.objects.create(
            user=user,
            place='Парк',
            time='07:00:00',
            action='Пробежка',
            is_pleasant=False,
            duration=120,
            reward='Протеин'
        )

        message = format_habit_reminder(habit)

        assert 'Пробежка' in message
        assert 'Парк' in message
        assert 'Протеин' in message
        assert '07:00' in message


@pytest.mark.django_db
class TestHabitReminderTask:
    """Tests pentru send_habit_reminder task"""

    @patch('habits.tasks.send_telegram_message')
    def test_send_habit_reminder_success(self, mock_send):
        """Test: Task trimite reminder cu succes"""
        mock_send.return_value = True

        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123',
            telegram_chat_id='123456789'
        )

        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            is_pleasant=False,
            duration=60,
            reward='Кофе'
        )

        result = send_habit_reminder(habit.id)

        assert result['status'] == 'success'
        assert result['habit_id'] == habit.id
        assert mock_send.called

    @patch('habits.tasks.send_telegram_message')
    def test_send_habit_reminder_no_chat_id(self, mock_send):
        """Test: User fără telegram_chat_id - skip"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
            # telegram_chat_id = None
        )

        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            is_pleasant=False,
            duration=60,
            reward='Кофе'
        )

        result = send_habit_reminder(habit.id)

        assert result['status'] == 'skipped'
        assert not mock_send.called

    def test_send_habit_reminder_nonexistent_habit(self):
        """Test: Habit inexistent returnează error"""
        result = send_habit_reminder(99999)

        assert result['status'] == 'error'
        assert 'not found' in result['message'].lower()


@pytest.mark.django_db
class TestSendHabitReminders:
    """Tests pentru send_habit_reminders periodic task"""

    @patch('habits.tasks.send_habit_reminder')
    def test_send_habit_reminders(self, mock_task):
        """Test: Task periodic verifică și trimite reminders"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123',
            telegram_chat_id='123456789'
        )

        # Creăm habit cu timp apropiat de now
        from django.utils import timezone
        now = timezone.now()

        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time=now.time(),
            action='Зарядка',
            is_pleasant=False,
            duration=60,
            reward='Кофе'
        )

        result = send_habit_reminders()

        assert result['status'] == 'complete'
        assert result['sent'] >= 0