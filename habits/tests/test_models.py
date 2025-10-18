import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()


@pytest.mark.django_db
class TestHabitModel:
    """Tests pentru Habit model"""

    def test_create_useful_habit_with_reward(self):
        """Test: Creare useful habit cu reward"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        habit = Habit.objects.create(
            user=user,
            place='Парк',
            time='07:00:00',
            action='Пробежка 2 км',
            is_pleasant=False,
            duration=120,
            periodicity=1,
            reward='Протеиновый коктейль'
        )

        assert habit.id is not None
        assert habit.action == 'Пробежка 2 км'
        assert habit.is_pleasant is False
        assert habit.reward == 'Протеиновый коктейль'
        assert habit.related_habit is None

    def test_create_pleasant_habit(self):
        """Test: Creare pleasant habit (fără reward/related)"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='20:00:00',
            action='Принять ванну с пеной',
            is_pleasant=True,
            duration=90,
            periodicity=1
        )

        assert habit.is_pleasant is True
        assert habit.reward is None
        assert habit.related_habit is None

    def test_create_useful_habit_with_related_pleasant_habit(self):
        """Test: Useful habit cu related pleasant habit"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        pleasant = Habit.objects.create(
            user=user,
            place='Дом',
            time='20:00:00',
            action='Посмотреть эпизод сериала',
            is_pleasant=True,
            duration=60
        )

        useful = Habit.objects.create(
            user=user,
            place='Квартира',
            time='19:00:00',
            action='Убрать комнату',
            is_pleasant=False,
            duration=30,
            related_habit=pleasant
        )

        assert useful.related_habit == pleasant
        assert useful.reward is None

    def test_habit_str_representation(self):
        """Test: __str__ method"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        habit = Habit.objects.create(
            user=user,
            place='Офис',
            time='14:00:00',
            action='Выпить воду',
            is_pleasant=False,
            duration=10,
            reward='Чувство свежести'
        )

        expected = 'Выпить воду в 14:00:00 (Офис)'
        assert str(habit) == expected

    def test_habit_default_periodicity(self):
        """Test: Default periodicity = 1 (zilnic)"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            is_pleasant=False,
            duration=60,
            reward='Бодрость'
        )

        assert habit.periodicity == 1

    def test_habit_default_is_public_false(self):
        """Test: Default is_public = False"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        habit = Habit.objects.create(
            user=user,
            place='Дом',
            time='08:00:00',
            action='Медитация',
            is_pleasant=False,
            duration=120,
            reward='Спокойствие'
        )

        assert habit.is_public is False


@pytest.mark.django_db
class TestHabitModelValidations:
    """Tests pentru validările Habit model"""

    def test_habit_with_both_reward_and_related_fails(self):
        """Test: Habit cu reward ȘI related_habit → ValidationError"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        pleasant = Habit.objects.create(
            user=user,
            place='Дом',
            time='20:00:00',
            action='Ванна',
            is_pleasant=True,
            duration=60
        )

        with pytest.raises(ValidationError) as exc_info:
            Habit.objects.create(
                user=user,
                place='Парк',
                time='07:00:00',
                action='Пробежка',
                is_pleasant=False,
                duration=120,
                reward='Протеин',
                related_habit=pleasant
            )

        assert 'одновременно' in str(exc_info.value).lower()

    def test_habit_duration_over_120_fails(self):
        """Test: Duration > 120 секунд → ValidationError"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        with pytest.raises(ValidationError) as exc_info:
            Habit.objects.create(
                user=user,
                place='Офис',
                time='14:00:00',
                action='Работа над проектом',
                is_pleasant=False,
                duration=150,  # > 120
                reward='Перерыв'
            )

        assert '120' in str(exc_info.value)

    def test_habit_periodicity_8_fails(self):
        """Test: Periodicity = 8 → ValidationError"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        with pytest.raises(ValidationError):
            Habit.objects.create(
                user=user,
                place='Дом',
                time='10:00:00',
                action='Уборка',
                is_pleasant=False,
                duration=60,
                periodicity=8,  # > 7
                reward='Чистота'
            )

    def test_pleasant_habit_with_reward_fails(self):
        """Test: Pleasant habit cu reward → ValidationError"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        with pytest.raises(ValidationError):
            Habit.objects.create(
                user=user,
                place='Дом',
                time='20:00:00',
                action='Ванна',
                is_pleasant=True,
                duration=90,
                reward='Релакс'  # Pleasant nu poate avea reward
            )

    def test_related_habit_not_pleasant_fails(self):
        """Test: Related habit cu is_pleasant=False → ValidationError"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        useful_habit = Habit.objects.create(
            user=user,
            place='Парк',
            time='08:00:00',
            action='Пробежка',
            is_pleasant=False,  # NOT pleasant
            duration=120,
            reward='Энергия'
        )

        with pytest.raises(ValidationError):
            Habit.objects.create(
                user=user,
                place='Дом',
                time='19:00:00',
                action='Уборка',
                is_pleasant=False,
                duration=30,
                related_habit=useful_habit  # Trebuie pleasant!
            )


@pytest.mark.django_db
class TestHabitModelMeta:
    """Tests pentru Meta options"""

    def test_habits_ordered_by_created_at_desc(self):
        """Test: Habits ordonate descrescător după created_at"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )

        habit1 = Habit.objects.create(
            user=user,
            place='A',
            time='08:00:00',
            action='First',
            is_pleasant=False,
            duration=60,
            reward='R1'
        )

        habit2 = Habit.objects.create(
            user=user,
            place='B',
            time='09:00:00',
            action='Second',
            is_pleasant=False,
            duration=60,
            reward='R2'
        )

        habits = list(Habit.objects.all())
        assert habits[0] == habit2  # Cel mai recent primul
        assert habits[1] == habit1